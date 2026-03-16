from __future__ import annotations

import allure

from stellar_burgers_api import endpoints as ep
from stellar_burgers_api.test_credentials import TEST_USER_EMAIL, TEST_USER_PASSWORD


def login_and_get_token(api) -> str | None:
    """Логин тестовым пользователем и получение accessToken."""
    with allure.step("PRE: POST /api/auth/login - получаем токен"):
        resp = api.post(ep.LOGIN, json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD})
    return resp.json.get("accessToken") if resp.json else None


def get_ingredient_ids(api, limit: int = 3) -> list[str]:
    """Получить список id ингредиентов."""
    with allure.step("PRE: GET /api/ingredients - получаем ингредиенты"):
        resp = api.get(ep.INGREDIENTS)
    data = (resp.json or {}).get("data") or []
    return [i["_id"] for i in data[:limit]]
