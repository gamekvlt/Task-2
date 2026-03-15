from __future__ import annotations

import uuid
import allure

from stellar_burgers_api import endpoints as ep
from stellar_burgers_api.data import unique_user_payload
from stellar_burgers_api.helpers import auth_header


def _new_email() -> str:
    return f"upd_{uuid.uuid4().hex}@example.com"


def _new_password() -> str:
    return f"newpass_{uuid.uuid4().hex}"


def _new_name() -> str:
    return f"NewName_{uuid.uuid4().hex[:8]}"


def _register_user(api, user_cleanup):
    payload = unique_user_payload()
    with allure.step("PRE: POST /api/auth/register - создаём пользователя"):
        resp = api.post(ep.REGISTER, json=payload)
    token = resp.json.get("accessToken") if resp.json else None
    user_cleanup(token)
    return token


@allure.feature("User")
@allure.story("Update user data")
class TestUserUpdate:
    @allure.title("Обновление email с авторизацией")
    def test_update_email_with_authorization(self, api, user_cleanup):
        token = _register_user(api, user_cleanup)
        new_val = _new_email()

        with allure.step("PATCH /api/auth/user - обновляем email"):
            resp = api.patch(ep.USER, headers=auth_header(token), json={"email": new_val})

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert resp.json.get("user", {}).get("email") == new_val

    @allure.title("Обновление name с авторизацией")
    def test_update_name_with_authorization(self, api, user_cleanup):
        token = _register_user(api, user_cleanup)
        new_val = _new_name()

        with allure.step("PATCH /api/auth/user - обновляем name"):
            resp = api.patch(ep.USER, headers=auth_header(token), json={"name": new_val})

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert resp.json.get("user", {}).get("name") == new_val

    @allure.title("Обновление password с авторизацией")
    def test_update_password_with_authorization(self, api, user_cleanup):
        token = _register_user(api, user_cleanup)
        new_val = _new_password()

        with allure.step("PATCH /api/auth/user - обновляем password"):
            resp = api.patch(ep.USER, headers=auth_header(token), json={"password": new_val})

        assert resp.status_code == 200
        assert resp.json.get("success") is True

    @allure.title("Обновление email без авторизации возвращает 401")
    def test_update_email_without_authorization(self, api):
        with allure.step("PATCH /api/auth/user - без токена"):
            resp = api.patch(ep.USER, json={"email": _new_email()})

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "You should be authorised"

    @allure.title("Обновление name без авторизации возвращает 401")
    def test_update_name_without_authorization(self, api):
        with allure.step("PATCH /api/auth/user - без токена"):
            resp = api.patch(ep.USER, json={"name": _new_name()})

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "You should be authorised"

    @allure.title("Обновление password без авторизации возвращает 401")
    def test_update_password_without_authorization(self, api):
        with allure.step("PATCH /api/auth/user - без токена"):
            resp = api.patch(ep.USER, json={"password": _new_password()})

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "You should be authorised"
