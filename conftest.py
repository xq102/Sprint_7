# conftest.py

import pytest
import allure
from api.scooter_api import CourierApi, OrderApi
from data import get_unique_courier_data, get_courier_payload_without_login, get_courier_payload_without_password, get_courier_payload_without_first_name, EXPECTED_MESSAGES, get_unique_order_data


@pytest.fixture
def base_courier_data():
    """Возвращает уникальные базовые данные курьера из data.py."""
    return get_unique_courier_data()


@pytest.fixture
def base_order_data():
    """Возвращает уникальные базовые данные заказа из data.py."""
    return get_unique_order_data()


@pytest.fixture
def courier_data_without_login():
    """Возвращает данные курьера без логина из data.py."""
    return get_courier_payload_without_login()


@pytest.fixture
def courier_data_without_password():
    """Возвращает данные курьера без пароля из data.py."""
    return get_courier_payload_without_password()


@pytest.fixture
def courier_data_without_first_name():
    """Возвращает данные курьера без firstName из data.py."""
    return get_courier_payload_without_first_name()


@pytest.fixture
def created_courier(base_courier_data):
    """Создаёт курьера, возвращает его ID. После теста удаляет курьера."""
    payload = base_courier_data
    response = CourierApi.create_courier(payload)
    if response.status_code != 201:
        pytest.fail(f"Failed to create courier. Status: {response.status_code}, Body: {response.text}")
    if not response.json().get("ok"):
        pytest.fail(f"Failed to create courier. Expected {{'ok': True}}, got {response.json()}. Body: {response.text}")

    created_courier_id = CourierApi.get_courier_id_by_login_pass(payload["login"], payload["password"])
    if created_courier_id is None:
        pytest.fail(f"Failed to get courier ID after creation. Login: {payload['login']}. Response: {response.text}")

    yield created_courier_id

    delete_response = CourierApi.delete_courier(created_courier_id)
    
    import logging
    if delete_response and delete_response.status_code not in [200, 404]:
        logging.warning(f"Failed to delete courier (ID: {created_courier_id}). Status: {delete_response.status_code}. Body: {delete_response.text}")
