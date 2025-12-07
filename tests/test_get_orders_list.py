# tests/test_get_orders_list.py

import allure
from api.scooter_api import OrderApi
from data import EXPECTED_RESPONSES


@allure.suite("Тесты на получение списка заказов")
class TestGetOrdersList:

    @allure.title("Получение списка заказов возвращает массив заказов и статус 200")
    def test_get_orders_list_returns_orders_array_200(self):
        response = OrderApi.get_orders_list()
        assert response.status_code == 200, \
            f"Ожидаемый статус код 200, получен {response.status_code}. Ответ: {response.text}"
        response_json = response.json()
        assert "orders" in response_json, \
            f"Поле 'orders' не найдено в ответе {response_json}. Ответ: {response.text}"
        assert isinstance(response_json["orders"], list), \
            f"Поле 'orders' должно быть списком, получено {type(response_json['orders'])}. Ответ: {response.text}"
