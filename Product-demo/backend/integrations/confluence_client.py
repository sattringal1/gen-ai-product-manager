"""
Confluence REST API v2 integration — publishes AI output as a page.
"""
import html
import httpx
import base64
import structlog
from config import settings

log = structlog.get_logger()


def _auth_header() -> dict:
    token = base64.b64encode(
        f"{settings.confluence_email}:{settings.confluence_api_token}".encode()
    ).decode()
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}


class ConfluenceClient:
    def __init__(self):
        self.base = settings.confluence_base_url.rstrip("/")
        self.space = settings.confluence_space_key
        self.enabled = bool(settings.confluence_api_token and self.base)

    async def publish_page(
        self,
        title: str,
        body: str,
        space_key: str | None = None,
    ) -> str | None:
        if not self.enabled:
            log.warning("confluence_disabled", reason="No credentials configured")
            return None

        space = space_key or self.space
        html_body = f"<pre>{html.escape(body)}</pre>"

        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space},
            "body": {
                "storage": {
                    "value": html_body,
                    "representation": "storage",
                }
            },
        }
        try:
            async with httpx.AsyncClient(headers=_auth_header(), timeout=30) as client:
                resp = await client.post(
                    f"{self.base}/rest/api/content", json=payload
                )
                resp.raise_for_status()
                data = resp.json()
                url = f"{self.base}/wiki{data['_links']['webui']}"
                log.info("confluence_page_created", url=url)
                return url
        except httpx.HTTPError as exc:
            log.error("confluence_error", error=type(exc).__name__, status=getattr(exc.response, 'status_code', None) if hasattr(exc, 'response') else None)
            return None
