from __future__ import annotations

import uuid

import allure
import pytest

from stellar_burgers_api import endpoints as ep


def _new_value(field: str) -> str:
    u = uuid.uuid4().hex
    if field == "email":
        return f"upd_{u}@example.com"
    if field == "password":
        return f"newpass_{u}"
    return f"NewName_{u[:8]}"


@allure.feature("User")
@allure.story("Update user data")
class TestUserUpdate:
    @allure.title("Обновление данных пользователя с авторизацией")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_update_user_with_authorization(self, api, registered_user, field):
        new_val = _new_value(field)
        headers = {"Authorization": registered_user["access_token"]}
        payload = {field: new_val}

        resp = api.patch(ep.USER, headers=headers, json=payload)

        assert resp.status_code == 200
        assert resp.json.get("success") is True

        # API возвращает обновлённые email/name, пароль в ответе не приходит
        if field in ("email", "name"):
            assert resp.json.get("user", {}).get(field) == new_val

    @allure.title("Обновление данных пользователя без авторизации возвращает 401")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_update_user_without_authorization(self, api, field):
        new_val = _new_value(field)
        payload = {field: new_val}

        resp = api.patch(ep.USER, json=payload)

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "You should be authorised"
