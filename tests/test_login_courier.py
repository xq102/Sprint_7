import allure
import pytest
from api.scooter_api import CourierApi
from data import EXPECTED_MESSAGES
from utils.helpers import generate_random_string


@allure.suite("Тесты на логин курьера")
class TestLoginCourier:

    def test_login_courier_with_correct_data_returns_id_200(self, base_courier_data):
        login = base_courier_data["login"]
        password = base_courier_data["password"]
        first_name = base_courier_data["firstName"]

        payload_create = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response_create = CourierApi.create_courier(payload_create)
        assert response_create.status_code == 201
        assert response_create.json() == {"ok": True}

        payload_login = {
            "login": login,
            "password": password
        }

        response_login = CourierApi.login_courier(payload_login)
        assert response_login.status_code == 200, \
            f"Ожидаемый статус код 200, получен {response_login.status_code}. Ответ: {response_login.text}"
        assert "id" in response_login.json(), \
            f"Поле 'id' не найдено в ответе {response_login.json()}. Ответ: {response_login.text}"

        courier_id = response_login.json().get("id")
        assert courier_id is not None, f"Не удалось получить ID курьера из ответа логина. Логин: {login}"
        delete_response = CourierApi.delete_courier(courier_id)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"

    def test_login_courier_without_login_returns_400_insufficient_data_message(self, base_courier_data):
        login = base_courier_data["login"]
        password = base_courier_data["password"]
        first_name = base_courier_data["firstName"]

        payload_create = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response_create = CourierApi.create_courier(payload_create)
        assert response_create.status_code == 201
        assert response_create.json() == {"ok": True}

        payload_login = {
            "password": password
        }

        response_login = CourierApi.login_courier(payload_login)
        assert response_login.status_code == 400, \
            f"Ожидаемый статус код 400, получен {response_login.status_code}. Ответ: {response_login.text}"
        expected_message = EXPECTED_MESSAGES["MISSING_LOGIN_OR_PASSWORD"]
        assert expected_message in response_login.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response_login.text}"

        courier_id = CourierApi.get_courier_id_by_login_pass(login, password)
        assert courier_id is not None, f"Не удалось получить ID курьера после его создания. Логин: {login}"
        delete_response = CourierApi.delete_courier(courier_id)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"

    def test_login_courier_without_password_returns_400_insufficient_data_message(self, base_courier_data):
        login = base_courier_data["login"]
        password = base_courier_data["password"]
        first_name = base_courier_data["firstName"]

        payload_create = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response_create = CourierApi.create_courier(payload_create)
        assert response_create.status_code == 201
        assert response_create.json() == {"ok": True}

        payload_login = {
            "login": login,
        }

        response_login = CourierApi.login_courier(payload_login)
        assert response_login.status_code == 400, \
            f"Ожидаемый статус код 400, получен {response_login.status_code}. Ответ: {response_login.text}"
        expected_message = EXPECTED_MESSAGES["MISSING_LOGIN_OR_PASSWORD"]
        assert expected_message in response_login.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response_login.text}"

        courier_id = CourierApi.get_courier_id_by_login_pass(login, password)
        assert courier_id is not None, f"Не удалось получить ID курьера после его создания. Логин: {login}"
        delete_response = CourierApi.delete_courier(courier_id)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"

    def test_login_courier_with_wrong_login_returns_404_account_not_found_message(self, base_courier_data):
        login = base_courier_data["login"]
        password = base_courier_data["password"]
        first_name = base_courier_data["firstName"]

        payload_create = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response_create = CourierApi.create_courier(payload_create)
        assert response_create.status_code == 201
        assert response_create.json() == {"ok": True}

        wrong_login = generate_random_string(10)
        payload_login = {
            "login": wrong_login,
            "password": password
        }

        response_login = CourierApi.login_courier(payload_login)
        assert response_login.status_code == 404, \
            f"Ожидаемый статус код 404, получен {response_login.status_code}. Ответ: {response_login.text}"
        expected_message = EXPECTED_MESSAGES["ACCOUNT_NOT_FOUND"]
        assert expected_message in response_login.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response_login.text}"

        courier_id = CourierApi.get_courier_id_by_login_pass(login, password)
        assert courier_id is not None, f"Не удалось получить ID курьера после его создания. Логин: {login}"
        delete_response = CourierApi.delete_courier(courier_id)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"

    def test_login_courier_with_wrong_password_returns_404_account_not_found_message(self, base_courier_data):
        login = base_courier_data["login"]
        password = base_courier_data["password"]
        first_name = base_courier_data["firstName"]

        payload_create = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response_create = CourierApi.create_courier(payload_create)
        assert response_create.status_code == 201
        assert response_create.json() == {"ok": True}

        wrong_password = generate_random_string(10)
        payload_login = {
            "login": login,
            "password": wrong_password
        }

        response_login = CourierApi.login_courier(payload_login)
        assert response_login.status_code == 404, \
            f"Ожидаемый статус код 404, получен {response_login.status_code}. Ответ: {response_login.text}"
        expected_message = EXPECTED_MESSAGES["ACCOUNT_NOT_FOUND"]
        assert expected_message in response_login.text, \
            f"Ожидаемое сообщение '{expected_message}' не найдено в ответе {response_login.text}"

        courier_id = CourierApi.get_courier_id_by_login_pass(login, password)
        assert courier_id is not None, f"Не удалось получить ID курьера после его создания. Логин: {login}"
        delete_response = CourierApi.delete_courier(courier_id)
        assert delete_response.status_code in [200, 404], \
            f"Удаление курьера (ID: {courier_id}) не вернуло 200 или 404. Статус: {delete_response.status_code}. Ответ: {delete_response.text}"
