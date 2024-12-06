import argparse
import asyncio
import os
import traceback
from typing import Optional, List, Dict, Any, Literal, AsyncGenerator
from dataclasses import dataclass
import aiohttp
from aiohttp.client_exceptions import ClientPayloadError
import json
import zipfile
import tempfile
from pathlib import Path
from github import Github, GithubException, Auth
from loguru import logger as log
import sys
from termcolor import colored
from tqdm import tqdm
from git import Repo, InvalidGitRepositoryError


def get_repo(path):
    try:
        Repo(path)
        return True
    except InvalidGitRepositoryError:
        return False


def loguru_formatter(record: Any) -> str:
    return (
        f"<green>{record['time']:YYYY-MM-DD HH:mm:ss} </green> "
        f"({record['elapsed'].total_seconds():>7.2f}s) | "
        f"<level>{record['level']: <8}</level> | "
        f"- <level>{record['message']}</level>\n"
    )


def setup_loguru():
    """Configure and return a logger instance with task-specific session ID"""
    # Remove default handlers
    log.remove()

    # Select the appropriate logging format
    logging_format = loguru_formatter

    log.add(
        "hackbot.log",
        format=logging_format,
        level="INFO",
        rotation="100kb",
        retention="10 days",
        backtrace=True,
    )
    log.add(
        lambda msg: tqdm.write(msg, end=""),
        colorize=True,
        format=logging_format,
        level="INFO",
    )


setup_loguru()


def url_format(address: str, port: Optional[int]) -> str:
    """Format the URL for the hackbot service."""
    scheme = address.split(":")[0]
    rest = address.split(":")[1]
    assert scheme in ["http", "https"], "Invalid URI scheme"
    return f"{scheme}:{rest}:{port}" if (port is not None) else f"{scheme}:{rest}"


@dataclass
class HackBotClientMessage:
    """A message sent to the hackbot client."""

    type: Literal["message", "progress", "error"]
    message: str

    def log(self) -> None:
        """Log the message to the console."""
        if self.type == "message":
            log.info(self.message)
        elif self.type == "progress":
            log.info(self.message, extra={"progress": True})
        elif self.type == "error":
            log.error(self.message)


async def process_stream(response: aiohttp.ClientResponse) -> AsyncGenerator[str, None]:
    """Process the streaming response from the hackbot service."""
    async for line in response.content:
        line = line.decode("utf-8")
        if line.startswith("data: "):
            try:
                json_str = line[5:].strip()  # Remove 'data: ' prefix
                yield json_str
            except json.JSONDecodeError:
                log.error(f"Failed to parse JSON: {json_str}")
    return


def compress_source_code(source_path: str, zip_path: str) -> None:
    """Compress the source code directory into a zip file."""
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_path):
                for file in files:
                    # Skip .zip files
                    if not file.endswith(".zip"):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)
        # Get zip file size
        zip_size = os.path.getsize(zip_path)
        log.debug(f"Created source code archive: {zip_size:,} bytes")
        if zip_size > 256 * 1024 * 1024:
            raise RuntimeError("Source code archive is too large to be scanned. Must be less than 256MB.")
    except Exception as e:
        raise RuntimeError(f"Failed to compress source code: {traceback.format_exc()}")


async def hack_target(address: str, port: int, api_key: str, source_path: str = ".", output: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Analyze the target source code using the hackbot service.

    Args:
        address: The hackbot service address
        port: The service port number
        api_key: Authentication API key
        source_path: Path to the source code to analyze
        output: Optional path to save results

    Returns:
        List of analysis results
    """
    # Compress the source code into a tempfile
    with tempfile.NamedTemporaryFile(delete=True, suffix=".zip") as temp_zip:
        compress_source_code(source_path, temp_zip.name)

        url = f"{url_format(address, port)}/api/hack"
        headers = {"X-API-KEY": api_key, "Connection": "keep-alive"}

        # Prepare the form data
        data = aiohttp.FormData()
        data.add_field(
            "file",
            open(temp_zip.name, "rb"),
            filename="compressed_source_code.zip",
            content_type="application/zip",
        )
        data.add_field("repo_url", "https://github.com/not_implemented")

        results = []
        timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status != 200:
                    raise RuntimeError(f"Hack request failed: {response.status}")

                async for result in process_stream(response):
                    results.append(json.loads(result))
                    yield result

                # Save results if output path specified
                if output:
                    output_path = Path(output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "w") as f:
                        json.dump(results, f, indent=2)

                return


async def cli_hack_target(address: str, port: int, api_key: str, source_path: str = ".", output: Optional[str] = None) -> None:

    results = []
    pbar = tqdm(desc=colored("\U0001F7E1" + " Analyzing code", "yellow"), unit=" findings")
    async for report in hack_target(address, port, api_key, source_path, output):
        result_json = json.loads(report)
        if result_json.get("message") is not None:
            log.info(result_json.get("message"))
            pbar.set_postfix_str(colored(result_json.get("message"), "yellow"))
        elif result_json.get("progress") is not None:
            pbar.set_postfix_str(colored(result_json.get("progress").get("message"), "yellow"))
        elif result_json.get("title") is not None:
            pbar.update(1)
            pbar.set_postfix_str(colored(result_json.get("title"), "yellow"))
            log.info("\U0001F41B Finding: " + colored(result_json.get("title"), "yellow"))
            results.append(result_json)
        elif result_json.get("error") is not None:
            pbar.close()
            print(colored(result_json.get("error"), "red"))
            return results
    pbar.close()

    if len(results) == 0:
        log.info(
            colored(
                "✅ No issues found",
                "green",
            )
        )

    return results


async def authenticate(address: str, port: int, api_key: str) -> bool:
    """Verify API key authentication with the hackbot service."""
    url = f"{url_format(address, port)}/api/authenticate"
    headers = {"X-API-KEY": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status == 200


async def generate_issues(issues_repo: str, github_api_key: str, results: List[Dict[str, Any]]) -> None:
    """
    Generate GitHub issues for bugs discovered by the bot.

    This function creates a master issue in the specified GitHub repository
    containing all the bugs found. It uses the GitHub API to create issues
    and requires appropriate authentication and permissions.

    Args:
        issues_repo (str): The full name of the GitHub repository (e.g., "owner/repo").
        github_api_key (str): The GitHub token for authentication.
        results (List[Dict[str, Any]]): A list of dictionaries containing bug information.

    Returns:
        None

    Raises:
        Exception: If there are permission issues or other errors when interacting with the GitHub API.

    Note:
        - This function requires a GitHub token with 'issues: write' and 'contents: read' permissions.
        - It creates a master issue with a title format of "HB-{number}".
    """
    if not issues_repo:
        log.error("GitHub repository is not specified.")
        return

    # Authenticate with GitHub
    auth = Auth.Token(github_api_key)
    g = Github(auth=auth)

    # Get a list of the bugs discovered by the bot
    issues_found = [issue for issue in results if issue.get("bug_id") is not None]
    if len(issues_found) == 0:
        log.info("No bugs found, skipping issue generation")
        return

    # Get the output repository. This will fail if the github token does not have access to the repository
    repo = None
    try:
        repo = g.get_repo(issues_repo)
    except GithubException as e:
        log.error(f"Error accessing repository: {e}")
        return

    last_hb_issue = 0
    # Fetch all existing issues in the repository and find the last one created by the bot
    for issue in repo.get_issues(state="all"):
        if issue.title.startswith("HB-"):
            last_hb_issue = int(issue.title.split("-")[1])
            break

    # Create a master issue in the repository that will contain all the bugs.
    # This will fail if the github token does not have write access to the issues
    # permissions:
    # - issues: write
    master_issue = None
    try:
        master_issue = repo.create_issue(title=f"HB-{last_hb_issue + 1}")
    except GithubException as e:
        log.error(f"Error creating issue: {e}")
        if e.status == 422:
            raise Exception("Validation failed, aborting. This functionality requires a GITHUB_TOKEN with 'issues: write' in the workflow permissions section.")
        elif e.status == 403:
            raise Exception("Forbidden, aborting. This functionality requires a GITHUB_TOKEN with 'issues: write' in the workflow permissions section.")
        elif e.status == 410:
            raise Exception("Gone, aborting. The repository does not allow issues.")

    # Add each bug as a comment to the master issue
    for issue in issues_found:
        body = f"#{issue.get('bug_id')} - {issue.get('bug_title')}\n{issue.get('bug_description')}"
        master_issue.create_comment(body=body)

    log.info(f"Created issue: {master_issue.title}")


def main() -> None:
    """CLI entrypoint for the hackbot tool."""
    parser = argparse.ArgumentParser(description="Hackbot - Eliminate bugs from your code")
    parser.add_argument(
        "--address",
        default="https://app.hackbot.org",
        help="Hackbot service address",
    )
    parser.add_argument("--port", type=int, default=None, required=False, help="Service port number")
    parser.add_argument(
        "--api-key",
        default=os.getenv("HACKBOT_API_KEY"),
        help="API key for authentication (default: HACKBOT_API_KEY environment variable)",
    )
    parser.add_argument(
        "--source",
        default=".",
        help="Path to source code directory (default: current directory)",
    )
    parser.add_argument("--output", help="Path to save analysis results")
    parser.add_argument("--auth-only", action="store_true", help="Only verify API key authentication")

    issue_parser = parser.add_argument_group("Issue Generation Options")
    issue_parser.add_argument(
        "--issues_repo",
        type=str,
        help="The repository to generate issues in (format: username/repo). By default empty and so no issues are generated",
    )
    issue_parser.add_argument(
        "--github_api_key",
        type=str,
        required=False,
        help="GitHub API key for issue generation",
    )

    args = parser.parse_args()

    # If no arguments passed, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    # Check that 1. the source folder is a git repo, and 2. it's a proper foundry project (foundry.toml exists)
    if not get_repo(args.source):
        log.error(f"❌ Error: The source folder is not the root of a git repository ({args.source} is not a git repository)")
        return 1
    if not os.path.exists(os.path.join(args.source, "foundry.toml")):
        log.error(f"❌ Error: The source folder is not the root of a proper foundry project (foundry.toml not found in {args.source})")
        return 1

    if not args.api_key:
        log.error("❌ Error: API key is required (either via --api-key or HACKBOT_API_KEY environment variable)")
        return 1

    # Run the async operations
    try:
        # Verify authentication
        if not asyncio.run(authenticate(args.address, args.port, args.api_key)):
            log.error("❌ Authentication failed")
            return 1

        log.info("✅ Authentication successful")

        if args.auth_only:
            return 0

        # Perform the analysis
        results = asyncio.run(cli_hack_target(args.address, args.port, args.api_key, args.source, args.output))

        if args.issues_repo:
            log.info(f"Generating issues report on repo {args.issues_repo}")
            asyncio.run(generate_issues(args.issues_repo, args.github_api_key, results))
        else:
            log.debug("No github repository for reporting issues has been specified. Skipping github issue generation.")

        # Give back result link url, which is just hackbot.org/dashboard/security-report#<session_id>
        # TODO

        # Output results to output-path
        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)

        return 0

    except ClientPayloadError:
        print(
            colored(
                "❌ The server terminated the connection prematurely, most likely due to an error in the scanning process. Check the streamed logs for error messages. Support: support@gatlingx.com",
                "red",
            )
        )
        return 1
    except Exception as e:
        if str(e) == "Hack request failed: 413":
            log.error("❌ The source code directory is too large to be scanned. Must be less than 256MB.")
        else:
            log.error(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
