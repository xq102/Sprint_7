import allure
import pytest
from api.scooter_api import CourierApi
from data import EXPECTED_RESPONSES, EXPECTED_MESSAGES
from utils.helpers import generate_random_string


@allure.suite("Тесты на создание курьера")
class TestCreateCourier:

    def test_create_courier_with_all_fields_returns_ok_true_201(self, base_courier_data):
        payload = base_courier_data
        response = CourierApi.create_courier(payload)
        assert response.status_code == 201, \
            f"Ожидаемый статус код 201, получен {response.status_code}. Ответ: {response.text}"
        assert response.json() == EXPECTED_RESPONSES["CREATE_COURIER_SUCCESS"], \
            f"Ожидаемый ответ {EXPECTED_RESPONSES['CREATE_COURIER_SUCCESS']}, получен {response.json()}. Ответ: {response.text}"
        courier_id = CourierApi.get_courier_id_by_login_pass(payload["login"], payload["password"])
        assert courier_id is not None, f"Не удалось получить ID курьера после его создания. Логин: {payload['login']}"
        delete_response = CourierApi.delete_courier(courier_id)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"

    def test_create_courier_with_duplicate_login_returns_400_or_409_duplicate_message(self, base_courier_data):
        login = base_courier_data["login"]
        password = base_courier_data["password"]
        first_name = base_courier_data["firstName"]

        payload1 = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        payload2 = {
            "login": login,
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response1 = CourierApi.create_courier(payload1)
        assert response1.status_code == 201
        assert response1.json() == {"ok": True}

        response2 = CourierApi.create_courier(payload2)
        assert response2.status_code in [400, 409], \
            f"Ожидаемый статус код 400 или 409, получен {response2.status_code}. Ответ: {response2.text}"
        expected_message = EXPECTED_MESSAGES["DUPLICATE_LOGIN"]
        assert expected_message in response2.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response2.text}"

        courier_id = CourierApi.get_courier_id_by_login_pass(login, password)
        assert courier_id is not None, f"Не удалось получить ID курьера после его создания. Логин: {login}"
        delete_response = CourierApi.delete_courier(courier_id)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"

    def test_create_courier_without_login_returns_400_insufficient_data_message(self, courier_data_without_login, expected_messages):
        payload = courier_data_without_login
        response = CourierApi.create_courier(payload)
        assert response.status_code == 400, \
            f"Ожидаемый статус код 400, получен {response.status_code}. Ответ: {response.text}"
        expected_message = expected_messages["MISSING_DATA_COURIER"]
        assert expected_message in response.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response.text}"

    def test_create_courier_without_password_returns_400_insufficient_data_message(self, courier_data_without_password, expected_messages):
        payload = courier_data_without_password
        response = CourierApi.create_courier(payload)
        assert response.status_code == 400, \
            f"Ожидаемый статус код 400, получен {response.status_code}. Ответ: {response.text}"
        expected_message = expected_messages["MISSING_DATA_COURIER"]
        assert expected_message in response.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response.text}"

    def test_create_courier_without_first_name_returns_ok_true_201_or_fixes_api(self, courier_data_without_first_name):
        payload = courier_data_without_first_name
        response = CourierApi.create_courier(payload)
        assert response.status_code == 201, \
            f"Ожидаемый статус код 201 (фактическое поведение API), получен {response.status_code}. Ответ: {response.text}"
        assert response.json() == {"ok": True}, \
            f"Ожидаемый ответ {'{'}'ok': True{'}'} (фактическое поведение API), получен {response.json()}. Ответ: {response.text}"
        courier_id = CourierApi.get_courier_id_by_login_pass(payload["login"], payload["password"])
        assert courier_id is not None, f"Не удалось получить ID курьера после его создания. Логин: {payload['login']}"
        delete_response = CourierApi.delete_courier(courier_id)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"
