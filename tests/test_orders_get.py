from __future__ import annotations

import allure

from stellar_burgers_api import endpoints as ep


@allure.feature("Orders")
@allure.story("Get user orders")
class TestOrdersGet:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized_user(self, api, registered_user, ingredients_ids):
        headers = {"Authorization": registered_user["access_token"]}

        create_resp = api.post(ep.ORDERS, headers=headers, json={"ingredients": ingredients_ids[:2]})
        assert create_resp.status_code == 200
        assert create_resp.json.get("success") is True

        resp = api.get(ep.ORDERS, headers=headers)

        assert resp.status_code == 200
        assert resp.json.get("success") is True
        assert "orders" in resp.json

    @allure.title("Получение заказов без авторизации возвращает 401")
    def test_get_orders_unauthorized_user(self, api):
        resp = api.get(ep.ORDERS)

        assert resp.status_code == 401
        assert resp.json.get("success") is False
        assert resp.json.get("message") == "You should be authorised"
