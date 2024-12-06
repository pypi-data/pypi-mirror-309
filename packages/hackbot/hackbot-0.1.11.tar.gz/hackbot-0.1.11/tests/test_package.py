import os
import pytest
from unittest.mock import patch, MagicMock
from src.hackbot import (
    authenticate,
    compress_source_code,
    hack_target,
    generate_issues,
)


@pytest.fixture
def test_params():
    return {
        "address": "http://test.example.com",
        "port": 8080,
        "api_key": "test_api_key",
        "source": "test_source",
    }


@pytest.mark.asyncio
@patch("src.hackbot.aiohttp.ClientSession")
async def test_authenticate_success(mock_session, test_params):
    # Create mock response
    mock_response = MagicMock(spec=["status", "json"])
    mock_response.status = 200
    mock_response.json.return_value = {"status": "authenticated"}

    # Setup session context manager
    mock_session_context = MagicMock()
    mock_session_context.__aenter__.return_value = mock_session_context
    mock_session_context.get.return_value.__aenter__.return_value = mock_response
    mock_session.return_value = mock_session_context

    result = await authenticate(test_params["address"], test_params["port"], test_params["api_key"])
    assert result is True

    # Updated assertion to use the mock_session_context directly
    expected_url = f"{test_params['address']}:{test_params['port']}/api/authenticate"
    expected_headers = {"X-API-KEY": test_params["api_key"]}
    mock_session_context.get.assert_called_once_with(
        expected_url,
        headers=expected_headers,
    )


@pytest.mark.asyncio
@patch("src.hackbot.aiohttp.ClientSession")
async def test_authenticate_failure(mock_session, test_params):
    # Create mock response
    mock_response = MagicMock(spec=["status", "json"])
    mock_response.status = 401
    mock_response.json.return_value = {"error": "unauthorized"}

    # Setup session context manager
    mock_session_context = MagicMock()
    mock_session_context.__aenter__.return_value = mock_session_context
    mock_session_context.get.return_value.__aenter__.return_value = mock_response
    mock_session.return_value = mock_session_context

    result = await authenticate(test_params["address"], test_params["port"], test_params["api_key"])
    assert result is False


def test_compress_source_code():
    # Create a temporary directory with some test files
    os.makedirs("test_src", exist_ok=True)
    with open("test_src/test_file.txt", "w") as f:
        f.write("Test content")

    compress_source_code("test_src", "src.zip")
    assert os.path.exists("src.zip")

    # Clean up
    os.remove("src.zip")
    os.remove("test_src/test_file.txt")
    os.rmdir("test_src")


@pytest.mark.asyncio
@patch("src.hackbot.aiohttp.ClientSession")
@patch("src.hackbot.compress_source_code")
async def test_hack_target(mock_compress, mock_session, test_params):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.content.__aiter__.return_value = [b'data: {"key": "value"}']

    mock_session_context = MagicMock()
    mock_session_context.__aenter__.return_value = mock_session_context
    mock_session_context.post.return_value.__aenter__.return_value = mock_response

    mock_session.return_value = mock_session_context

    results = []
    async for result in hack_target(
        test_params["address"], test_params["port"], test_params["api_key"], test_params["source"]
    ):
        results.append(result)
    assert results == ['{"key": "value"}']


@pytest.mark.asyncio
@patch("src.hackbot.Github")
async def test_generate_issues(mock_github):
    mock_repo = MagicMock()
    mock_issue = MagicMock()
    mock_issue.title = "HB-1"
    mock_repo.get_issues.return_value = [mock_issue]
    mock_repo.create_issue.return_value = mock_issue

    mock_github.return_value.get_repo.return_value = mock_repo

    issues = [
        {
            "bug_id": "BUG-1",
            "bug_title": "Test Bug",
            "bug_description": "This is a test bug",
        }
    ]
    await generate_issues("test_owner/test_repo", "test_github_api_key", issues)

    mock_repo.create_issue.assert_called_once_with(title="HB-2")
    mock_issue.create_comment.assert_called_once_with(body="#BUG-1 - Test Bug\nThis is a test bug")
