from __future__ import annotations

import allure
import pytest

from stellar_burgers_api import endpoints as ep
from stellar_burgers_api.test_credentials import TEST_USER_EMAIL, TEST_USER_PASSWORD


@allure.feature("User")
@allure.story("Login")
class TestUserLogin:
    @allure.title("Логин существующего пользователя (тестовые креды из проекта)")
    def test_login_with_static_test_credentials_success(self, api):
        resp = api.post(ep.LOGIN, json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD})

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert "accessToken" in resp.json
        assert "refreshToken" in resp.json
        assert resp.json.get("user", {}).get("email") == TEST_USER_EMAIL

    @allure.title("Логин под существующим пользователем (созданным в тесте)")
    def test_login_existing_user_success(self, api, registered_user):
        resp = api.post(ep.LOGIN, json={"email": registered_user["email"], "password": registered_user["password"]})

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert "accessToken" in resp.json
        assert "refreshToken" in resp.json
        assert resp.json.get("user", {}).get("email") == registered_user["email"]

    @allure.title("Логин с неверным логином/паролем возвращает 401")
    @pytest.mark.parametrize(
        "case",
        ["wrong_password", "wrong_email"],
    )
    def test_login_invalid_credentials(self, api, registered_user, case):
        email = registered_user["email"]
        password = registered_user["password"]

        if case == "wrong_password":
            password = "wrong_password"
        if case == "wrong_email":
            email = "wrong_email@example.com"

        resp = api.post(ep.LOGIN, json={"email": email, "password": password})

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "email or password are incorrect"
