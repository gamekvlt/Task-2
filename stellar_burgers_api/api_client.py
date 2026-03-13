from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    json: Optional[Dict[str, Any]]
    text: str


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> ApiResponse:
        url = f"{self.base_url}{path}"
        resp = self.session.request(method, url, headers=headers, json=json, timeout=20)
        data = None
        try:
            data = resp.json()
        except ValueError:
            data = None
        return ApiResponse(status_code=resp.status_code, json=data, text=resp.text)


def get(self, path: str, *, headers: Optional[Dict[str, str]] = None) -> ApiResponse:
    return self.request("GET", path, headers=headers)

def post(
    self,
    path: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> ApiResponse:
    return self.request("POST", path, headers=headers, json=json)

def patch(
    self,
    path: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> ApiResponse:
    return self.request("PATCH", path, headers=headers, json=json)

def delete(self, path: str, *, headers: Optional[Dict[str, str]] = None) -> ApiResponse:
    return self.request("DELETE", path, headers=headers)
