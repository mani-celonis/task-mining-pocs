"""
Jira Cloud REST / Agile API client (read-only).
Auth: email + API token (HTTP Basic). Retries on 429 like AhaApiClient.
"""

import time
from typing import Any, Dict, List, Optional, Union

import requests
from requests.auth import HTTPBasicAuth

USER_AGENT = "Celonis PM Automation (Agent)"


def normalize_jira_host(host: str) -> str:
    h = (host or "").strip().rstrip("/")
    if not h.startswith("http"):
        h = "https://" + h
    return h


class JiraApiClient:
    def __init__(self, host: str, email: str, api_token: str):
        self.base_url = normalize_jira_host(host)
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(email, api_token)
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            }
        )

    def get(
        self, path: str, params: Optional[Dict[str, Union[str, int]]] = None
    ) -> Any:
        if not path.startswith("/"):
            path = "/" + path
        url = f"{self.base_url}{path}"
        while True:
            resp = self.session.get(url, params=params)
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "60")
                delay = int(retry_after) if str(retry_after).isdigit() else 60
                time.sleep(delay)
                continue
            resp.raise_for_status()
            if resp.status_code == 204 or not resp.content:
                return None
            return resp.json()

    def get_fields(self) -> List[Dict[str, Any]]:
        """All issue fields (site-specific IDs for Epic Link, etc.)."""
        data = self.get("/rest/api/3/field")
        if not isinstance(data, list):
            return []
        return data

    def search_issues(
        self, jql: str, field_ids: List[str], max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Paginate GET /rest/api/3/search/jql (Jira Cloud; legacy GET /search returns 410).
        Uses nextPageToken when present.
        """
        out: List[Dict[str, Any]] = []
        fields_param = ",".join(field_ids)
        next_token: Optional[str] = None
        while True:
            params: Dict[str, Union[str, int]] = {
                "jql": jql,
                "maxResults": max_results,
                "fields": fields_param,
            }
            if next_token:
                params["nextPageToken"] = next_token
            data = self.get("/rest/api/3/search/jql", params=params)
            issues = data.get("issues") or []
            out.extend(issues)
            next_token = data.get("nextPageToken") or None
            if not next_token or not issues:
                break
        return out
