import pytest
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
def expected_messages():
    """Возвращает словарь с ожидаемыми сообщениями об ошибках из data.py."""
    return EXPECTED_MESSAGES

 
@pytest.fixture
def created_courier(base_courier_data): 
    """Создаёт курьера, возвращает его данные. После теста удаляет курьера."""
    payload = base_courier_data 
    response = CourierApi.create_courier(payload)
    assert response.status_code == 201
    assert response.json() == {"ok": True}

    created_data = {
        "login": payload["login"],
        "password": payload["password"],
        "firstName": payload["firstName"]
    }

    yield created_data

    if created_data: 
        courier_id = CourierApi.get_courier_id_by_login_pass(created_data["login"], created_data["password"])
        if courier_id is not None:
            delete_response = CourierApi.delete_courier(courier_id)
