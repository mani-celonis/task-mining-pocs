"""
Base Aha! REST API client.
Handles auth, headers, and rate limiting per .cursorrules.
"""

import time
from typing import Any, Dict, Optional

import requests

BASE_URL = "https://celonis.aha.io/api/v1"
USER_AGENT = "Celonis PM Automation (Agent)"


class AhaApiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            }
        )

    def get(self, path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        url = f"{BASE_URL}{path}"
        while True:
            resp = self.session.get(url, params=params)
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "60")
                delay = int(retry_after) if retry_after.isdigit() else 60
                time.sleep(delay)
                continue
            resp.raise_for_status()
            return resp.json()

    def put(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{BASE_URL}{path}"
        while True:
            resp = self.session.put(url, json=data)
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "60")
                delay = int(retry_after) if retry_after.isdigit() else 60
                time.sleep(delay)
                continue
            resp.raise_for_status()
            return resp.json()

    def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{BASE_URL}{path}"
        while True:
            resp = self.session.post(url, json=data)
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "60")
                delay = int(retry_after) if retry_after.isdigit() else 60
                time.sleep(delay)
                continue
            resp.raise_for_status()
            return resp.json()

    def delete(self, path: str) -> None:
        url = f"{BASE_URL}{path}"
        while True:
            resp = self.session.delete(url)
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After", "60")
                delay = int(retry_after) if retry_after.isdigit() else 60
                time.sleep(delay)
                continue
            resp.raise_for_status()
            return
