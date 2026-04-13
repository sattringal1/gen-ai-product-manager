"""
Jira REST API v3 integration — creates epics and user stories.
"""
import httpx
import base64
import structlog
from config import settings

log = structlog.get_logger()


def _auth_header() -> dict:
    token = base64.b64encode(
        f"{settings.jira_email}:{settings.jira_api_token}".encode()
    ).decode()
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}


class JiraClient:
    def __init__(self):
        self.base = settings.jira_base_url.rstrip("/")
        self.project = settings.jira_project_key
        self.enabled = bool(settings.jira_api_token and self.base)

    async def _post(self, path: str, payload: dict) -> dict:
        async with httpx.AsyncClient(headers=_auth_header(), timeout=30) as client:
            resp = await client.post(f"{self.base}{path}", json=payload)
            resp.raise_for_status()
            return resp.json()

    async def create_epic(self, name: str, summary: str, project_key: str) -> str:
        """Creates an epic and returns its issue key."""
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": "Epic"},
                "customfield_10014": name,  # Epic Name field
            }
        }
        result = await self._post("/rest/api/3/issue", payload)
        return result["key"]

    async def create_story(
        self,
        story: dict,
        project_key: str,
        epic_key: str | None = None,
    ) -> str:
        """Creates a user story and returns its key."""
        description_text = (
            f"As a {story.get('as_a')}, "
            f"I want {story.get('i_want')}, "
            f"so that {story.get('so_that')}.\n\n"
            "Acceptance Criteria:\n"
        )
        for ac in story.get("acceptance_criteria", []):
            description_text += (
                f"- GIVEN {ac['given']} WHEN {ac['when']} THEN {ac['then']}\n"
            )

        fields: dict = {
            "project": {"key": project_key},
            "summary": story["title"],
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description_text}],
                    }
                ],
            },
            "issuetype": {"name": "Story"},
            "priority": {"name": story.get("priority", "Medium")},
            "story_points": story.get("story_points", 3),
        }
        if epic_key:
            fields["customfield_10014"] = epic_key  # Epic Link

        payload = {"fields": fields}
        result = await self._post("/rest/api/3/issue", payload)
        return result["key"]

    async def create_stories(
        self, output: dict, project_key: str | None = None
    ) -> list[str]:
        """Creates epic + all stories from UserStorySet output. Returns issue keys."""
        if not self.enabled:
            log.warning("jira_disabled", reason="No credentials configured")
            return []

        project_key = project_key or self.project
        keys: list[str] = []

        try:
            epic_key = await self.create_epic(
                name=output.get("epic_name", "AI Generated Epic"),
                summary=output.get("epic_summary", ""),
                project_key=project_key,
            )
            keys.append(epic_key)
            log.info("jira_epic_created", key=epic_key)

            for story in output.get("stories", []):
                key = await self.create_story(story, project_key, epic_key)
                keys.append(key)
                log.info("jira_story_created", key=key)

        except httpx.HTTPError as exc:
            log.error("jira_error", error=type(exc).__name__, status=getattr(exc.response, 'status_code', None) if hasattr(exc, 'response') else None)

        return keys
