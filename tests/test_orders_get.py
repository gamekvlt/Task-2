from __future__ import annotations

import allure

from stellar_burgers_api import endpoints as ep
from stellar_burgers_api.test_credentials import TEST_USER_EMAIL, TEST_USER_PASSWORD
from stellar_burgers_api.helpers import auth_header


def _login_and_token(api):
    with allure.step("PRE: POST /api/auth/login - получаем токен"):
        resp = api.post(ep.LOGIN, json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD})
    return resp.json.get("accessToken") if resp.json else None


def _get_ingredient_ids(api):
    with allure.step("PRE: GET /api/ingredients - получаем ингредиенты"):
        resp = api.get(ep.INGREDIENTS)
    data = (resp.json or {}).get("data") or []
    return [i["_id"] for i in data[:3]]


@allure.feature("Orders")
@allure.story("Get user orders")
class TestOrdersGet:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized_user(self, api):
        token = _login_and_token(api)
        ingredient_ids = _get_ingredient_ids(api)

        with allure.step("PRE: POST /api/orders - создаём заказ"):
            api.post(ep.ORDERS, headers=auth_header(token), json={"ingredients": ingredient_ids[:2]})

        with allure.step("GET /api/orders - получаем заказы"):
            resp = api.get(ep.ORDERS, headers=auth_header(token))

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert "orders" in resp.json

    @allure.title("Получение заказов без авторизации возвращает 401")
    def test_get_orders_unauthorized_user(self, api):
        with allure.step("GET /api/orders - без токена"):
            resp = api.get(ep.ORDERS)

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "You should be authorised"
