import allure
import pytest
from api.scooter_api import OrderApi
from data import ORDER_COLORS


@allure.suite("Тесты на создание заказа")
class TestCreateOrder:

    @pytest.mark.parametrize("color", ORDER_COLORS, ids=["color_BLACK", "color_GREY", "color_BLACK_GREY", "no_color"])
    @allure.title("Тест: Создание заказа с цветом {color} возвращает трек-номер и статус 201")
    def test_create_order_with_color_returns_track_201(self, base_order_data, color):
        payload = base_order_data.copy()
        if color:
            payload["color"] = color

        response = OrderApi.create_order(payload)
        assert response.status_code == 201, \
            f"Ожидаемый статус код 201, получен {response.status_code}. Ответ: {response.text}"
        assert "track" in response.json(), \
            f"Поле 'track' не найдено в ответе {response.json()}. Ответ: {response.text}"
