from __future__ import annotations

import allure

from stellar_burgers_api import endpoints as ep


@allure.feature("Orders")
@allure.story("Create order")
class TestOrderCreate:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth(self, api, registered_user, ingredients_ids):
        headers = {"Authorization": registered_user["access_token"]}
        payload = {"ingredients": ingredients_ids[:2]}

        resp = api.post(ep.ORDERS, headers=headers, json=payload)

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert resp.json.get("order", {}).get("number") is not None

    @allure.title("Создание заказа без авторизации и с ингредиентами")
    def test_create_order_without_auth(self, api, ingredients_ids):
        payload = {"ingredients": ingredients_ids[:2]}

        resp = api.post(ep.ORDERS, json=payload)

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert resp.json.get("order", {}).get("number") is not None

    @allure.title("Создание заказа без ингредиентов возвращает 400")
    def test_create_order_without_ingredients(self, api):
        resp = api.post(ep.ORDERS, json={"ingredients": []})

        assert resp.status_code == 400
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "Ingredient ids must be provided"

    @allure.title("Создание заказа с невалидным хешем ингредиента возвращает 500")
    def test_create_order_with_invalid_ingredient_hash(self, api):
        resp = api.post(ep.ORDERS, json={"ingredients": ["invalid_hash"]})

        assert resp.status_code == 500
