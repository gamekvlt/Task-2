from __future__ import annotations

import allure
import pytest

from stellar_burgers_api import endpoints as ep


@allure.feature("User")
@allure.story("Create user")
class TestUserCreate:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api, user_cleanup, new_user_payload):
        with allure.step("POST /api/auth/register - создаём пользователя"):
            resp = api.post(ep.REGISTER, json=new_user_payload)

        user_cleanup(resp.json.get("accessToken") if resp.json else None)

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert resp.json.get("user", {}).get("email") == new_user_payload["email"]
        assert resp.json.get("user", {}).get("name") == new_user_payload["name"]
        assert "accessToken" in resp.json
        assert "refreshToken" in resp.json

    @allure.title("Создание уже зарегистрированного пользователя возвращает 403")
    def test_create_user_already_registered(self, api, user_cleanup, new_user_payload):
        with allure.step("PRE: POST /api/auth/register - создаём пользователя"):
            pre = api.post(ep.REGISTER, json=new_user_payload)
        user_cleanup(pre.json.get("accessToken") if pre.json else None)

        with allure.step("POST /api/auth/register - повторная регистрация"):
            resp = api.post(ep.REGISTER, json=new_user_payload)

        assert resp.status_code == 403
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "User already exists"

    @allure.title("Создание пользователя без обязательного поля возвращает 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, api, new_user_payload, missing_field):
        new_user_payload.pop(missing_field)

        with allure.step(f"POST /api/auth/register - регистрация без поля {missing_field}"):
            resp = api.post(ep.REGISTER, json=new_user_payload)

        assert resp.status_code == 403
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "Email, password and name are required fields"
