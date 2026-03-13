from __future__ import annotations

import allure
import pytest

from stellar_burgers_api.data import unique_user_payload
from stellar_burgers_api import endpoints as ep


@allure.feature("User")
@allure.story("Create user")
class TestUserCreate:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api, user_cleanup):
        payload = unique_user_payload()

        resp = api.post(ep.REGISTER, json=payload)

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert resp.json.get("user", {}).get("email") == payload["email"]
        assert resp.json.get("user", {}).get("name") == payload["name"]
        assert "accessToken" in resp.json
        assert "refreshToken" in resp.json

        user_cleanup(resp.json.get("accessToken"))

    @allure.title("Создание пользователя, который уже зарегистрирован, возвращает 403")
    def test_create_user_already_registered(self, api, user_cleanup):
        payload = unique_user_payload()

        resp1 = api.post(ep.REGISTER, json=payload)

        assert resp1.status_code == 200
        assert resp1.json.get("success") is True

        user_cleanup(resp1.json.get("accessToken"))

        resp2 = api.post(ep.REGISTER, json=payload)

        assert resp2.status_code == 403
        assert resp2.json.get("success") is False
        assert resp2.json.get("message") == "User already exists"

    @allure.title("Создание пользователя без обязательного поля возвращает 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, api, missing_field):
        payload = unique_user_payload()
        payload.pop(missing_field)

        resp = api.post(ep.REGISTER, json=payload)

        assert resp.status_code == 403
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "Email, password and name are required fields"
