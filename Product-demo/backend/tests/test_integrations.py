"""
Tests for Jira and Confluence integration clients.
Uses respx to mock HTTP calls.
"""
import pytest
import respx
import httpx
from unittest.mock import patch, MagicMock

from tests.conftest import MOCK_USER_STORIES


# ── Jira ──────────────────────────────────────────────────────────────────────

class TestJiraClient:
    def _make_client(self, base_url="https://test.atlassian.net", token="test-token"):
        with patch("integrations.jira_client.settings") as mock_settings:
            mock_settings.jira_base_url = base_url
            mock_settings.jira_email = "test@example.com"
            mock_settings.jira_api_token = token
            mock_settings.jira_project_key = "PM"
            from integrations.jira_client import JiraClient
            return JiraClient()

    def test_disabled_when_no_token(self):
        from integrations.jira_client import JiraClient
        with patch("integrations.jira_client.settings") as s:
            s.jira_api_token = ""
            s.jira_base_url = "https://x.atlassian.net"
            s.jira_project_key = "PM"
            client = JiraClient()
        assert not client.enabled

    def test_enabled_when_credentials_present(self):
        client = self._make_client()
        assert client.enabled

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_epic_returns_key(self):
        respx.post("https://test.atlassian.net/rest/api/3/issue").mock(
            return_value=httpx.Response(201, json={"key": "PM-1", "id": "10001"})
        )
        client = self._make_client()
        key = await client.create_epic("Test Epic", "Epic summary", "PM")
        assert key == "PM-1"

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_story_returns_key(self):
        respx.post("https://test.atlassian.net/rest/api/3/issue").mock(
            return_value=httpx.Response(201, json={"key": "PM-2", "id": "10002"})
        )
        client = self._make_client()
        story = MOCK_USER_STORIES["stories"][0]
        key = await client.create_story(story, "PM", "PM-1")
        assert key == "PM-2"

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_stories_returns_all_keys(self):
        respx.post("https://test.atlassian.net/rest/api/3/issue").mock(
            side_effect=[
                httpx.Response(201, json={"key": "PM-10"}),
                httpx.Response(201, json={"key": "PM-11"}),
            ]
        )
        client = self._make_client()
        keys = await client.create_stories(MOCK_USER_STORIES, "PM")
        assert "PM-10" in keys

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_jira_http_error_gracefully(self):
        respx.post("https://test.atlassian.net/rest/api/3/issue").mock(
            return_value=httpx.Response(401, json={"message": "Unauthorized"})
        )
        client = self._make_client()
        keys = await client.create_stories(MOCK_USER_STORIES, "PM")
        assert keys == []


# ── Confluence ────────────────────────────────────────────────────────────────

class TestConfluenceClient:
    def _make_client(self, token="test-token"):
        with patch("integrations.confluence_client.settings") as s:
            s.confluence_base_url = "https://test.atlassian.net/wiki"
            s.confluence_email = "test@example.com"
            s.confluence_api_token = token
            s.confluence_space_key = "PROD"
            from integrations.confluence_client import ConfluenceClient
            return ConfluenceClient()

    def test_disabled_when_no_token(self):
        from integrations.confluence_client import ConfluenceClient
        with patch("integrations.confluence_client.settings") as s:
            s.confluence_api_token = ""
            s.confluence_base_url = "https://x.atlassian.net/wiki"
            s.confluence_space_key = "PROD"
            client = ConfluenceClient()
        assert not client.enabled

    @pytest.mark.asyncio
    @respx.mock
    async def test_publish_page_returns_url(self):
        respx.post("https://test.atlassian.net/wiki/rest/api/content").mock(
            return_value=httpx.Response(200, json={
                "_links": {"webui": "/spaces/PROD/pages/12345"}
            })
        )
        client = self._make_client()
        url = await client.publish_page("Test Title", "Test body")
        assert url is not None
        assert "12345" in url

    @pytest.mark.asyncio
    @respx.mock
    async def test_returns_none_on_error(self):
        respx.post("https://test.atlassian.net/wiki/rest/api/content").mock(
            return_value=httpx.Response(403, json={"message": "Forbidden"})
        )
        client = self._make_client()
        url = await client.publish_page("Test", "body")
        assert url is None
