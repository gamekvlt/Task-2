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
@allure.story("Create order")
class TestOrderCreate:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, api):
        token = _login_and_token(api)
        ingredient_ids = _get_ingredient_ids(api)

        with allure.step("POST /api/orders - создаём заказ"):
            resp = api.post(ep.ORDERS, headers=auth_header(token), json={"ingredients": ingredient_ids[:2]})

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert resp.json.get("order", {}).get("number") is not None

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api):
        ingredient_ids = _get_ingredient_ids(api)

        with allure.step("POST /api/orders - создаём заказ без токена"):
            resp = api.post(ep.ORDERS, json={"ingredients": ingredient_ids[:2]})

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert resp.json.get("order", {}).get("number") is not None

    @allure.title("Создание заказа без ингредиентов возвращает 400")
    def test_create_order_without_ingredients(self, api):
        with allure.step("POST /api/orders - без ingredients"):
            resp = api.post(ep.ORDERS, json={"ingredients": []})

        assert resp.status_code == 400
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов возвращает 500")
    def test_create_order_with_invalid_ingredient_hash(self, api):
        with allure.step("POST /api/orders - неверный ingredients"):
            resp = api.post(ep.ORDERS, json={"ingredients": ["invalid_hash"]})

        assert resp.status_code == 500
