from __future__ import annotations

import allure

from stellar_burgers_api import endpoints as ep
from stellar_burgers_api.test_credentials import TEST_USER_EMAIL, TEST_USER_PASSWORD


@allure.feature("User")
@allure.story("Login")
class TestUserLogin:
    @allure.title("Логин существующего пользователя (тестовые креды из проекта)")
    def test_login_with_static_test_credentials_success(self, api):
        with allure.step("POST /api/auth/login - логин"):
            resp = api.post(ep.LOGIN, json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD})

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert "accessToken" in resp.json
        assert "refreshToken" in resp.json
        assert resp.json.get("user", {}).get("email") == TEST_USER_EMAIL

    @allure.title("Логин с неверным паролем возвращает 401")
    def test_login_wrong_password_returns_401(self, api):
        with allure.step("POST /api/auth/login - неверный пароль"):
            resp = api.post(ep.LOGIN, json={"email": TEST_USER_EMAIL, "password": "wrong_password"})

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "email or password are incorrect"

    @allure.title("Логин с неверным email возвращает 401")
    def test_login_wrong_email_returns_401(self, api):
        with allure.step("POST /api/auth/login - неверный email"):
            resp = api.post(ep.LOGIN, json={"email": "wrong_email@example.com", "password": TEST_USER_PASSWORD})

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "email or password are incorrect"
