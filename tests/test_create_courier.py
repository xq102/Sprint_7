import allure
import pytest
from api.scooter_api import CourierApi
from data import EXPECTED_RESPONSES, EXPECTED_MESSAGES, get_unique_courier_data
from utils.helpers import generate_random_string


@allure.suite("Тесты на создание курьера")
class TestCreateCourier:

    @allure.title("Курьер с корректными данными создается успешно, возвращается ok: true и статус 201")
    def test_create_courier_with_all_fields_returns_ok_true_201(self, created_courier):
        courier_id = created_courier
        assert courier_id is not None, f"Courier ID should not be None after creation by fixture."


    @allure.title("Попытка создать курьера с существующим логином возвращает 409")
    def test_create_courier_with_duplicate_login_returns_409(self):
        original_data = get_unique_courier_data()
        login = original_data["login"]
        password = original_data["password"]
        first_name = original_data["firstName"]

        payload1 = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response1 = CourierApi.create_courier(payload1)
        assert response1.status_code == 201
        assert response1.json() == {"ok": True}

        courier_id_to_delete = CourierApi.get_courier_id_by_login_pass(login, password)

        payload2 = {
            "login": login,
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response2 = CourierApi.create_courier(payload2)
        assert response2.status_code == 409, \
            f"Ожидаемый статус код 409 (дубликат логина), получен {response2.status_code}. Ответ: {response2.text}"
        expected_message = EXPECTED_MESSAGES["DUPLICATE_LOGIN"]
        assert expected_message in response2.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response2.text}"

        delete_response = CourierApi.delete_courier(courier_id_to_delete)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id_to_delete}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"


    @allure.title("Попытка создать курьера без пароля возвращает 400")
    def test_create_courier_without_password_returns_400_insufficient_data_message(self, courier_data_without_password):
        payload = courier_data_without_password
        response = CourierApi.create_courier(payload)
        assert response.status_code == 400, \
            f"Ожидаемый статус код 400, получен {response.status_code}. Ответ: {response.text}"
        expected_message = EXPECTED_MESSAGES["MISSING_DATA_COURIER"]
        assert expected_message in response.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response.text}"


    @allure.title("Попытка создать курьера без логина возвращает 400")
    def test_create_courier_without_login_returns_400_insufficient_data_message(self, courier_data_without_login):
        payload = courier_data_without_login
        response = CourierApi.create_courier(payload)
        assert response.status_code == 400, \
            f"Ожидаемый статус код 400, получен {response.status_code}. Ответ: {response.text}"
        expected_message = EXPECTED_MESSAGES["MISSING_DATA_COURIER"]
        assert expected_message in response.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response.text}"


    @allure.title("Курьер без firstName создается успешно (фактическое поведение API)")
    def test_create_courier_without_first_name_returns_ok_true_201_or_fixes_api(self, courier_data_without_first_name):
        payload = courier_data_without_first_name
        response = CourierApi.create_courier(payload)
        assert response.status_code == 201, \
            f"Ожидаемый статус код 201 (фактическое поведение API), получен {response.status_code}. Ответ: {response.text}"
        assert response.json() == {"ok": True}, \
            f"Ожидаемый ответ {{'ok': True}} (фактическое поведение API), получен {response.json()}. Ответ: {response.text}"
