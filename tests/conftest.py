from __future__ import annotations

import os
from typing import Dict, Generator, List, Callable

import allure
import pytest
import requests

from stellar_burgers_api.api_client import ApiClient
from stellar_burgers_api.data import unique_user_payload
from stellar_burgers_api import endpoints as ep


def auth_header(access_token: str) -> Dict[str, str]:
    return {"Authorization": access_token}


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("STELLAR_BURGERS_URL", "https://stellarburgers.education-services.ru").rstrip("/")


@pytest.fixture(scope="session")
def api(base_url: str) -> ApiClient:
    return ApiClient(base_url)


@pytest.fixture
def user_cleanup(api: ApiClient) -> Generator[Callable[[str | None], None], None, None]:
    """Collect access tokens created during a test and delete users afterwards."""
    tokens: List[str] = []

    def add(access_token: str | None) -> None:
        if access_token:
            tokens.append(access_token)

    yield add

    for token in tokens:
        try:
            api.delete(ep.USER, headers=auth_header(token))
        except requests.exceptions.RequestException:
            # cleanup must not fail a test run
            pass


@pytest.fixture
def ingredients_ids(api: ApiClient) -> List[str]:
    with allure.step("Получаем список ингредиентов"):
        resp = api.get(ep.INGREDIENTS)

    assert resp.status_code == 200
    assert resp.json and resp.json.get("success") is True

    data = resp.json.get("data") or []
    assert len(data) >= 1

    return [item["_id"] for item in data[:3]]


@pytest.fixture
def registered_user(api: ApiClient, user_cleanup) -> Dict[str, str]:
    payload = unique_user_payload()

    with allure.step("Создаём пользователя для теста"):
        resp = api.post(ep.REGISTER, json=payload)

    assert resp.status_code == 200
    assert resp.json and resp.json.get("success") is True
    assert "accessToken" in resp.json and "refreshToken" in resp.json

    access_token = resp.json["accessToken"]
    user_cleanup(access_token)

    return {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "access_token": access_token,
        "refresh_token": resp.json["refreshToken"],
    }
