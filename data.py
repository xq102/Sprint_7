from utils.helpers import generate_random_string


# --- Ожидаемые сообщения об ошибках ---
EXPECTED_MESSAGES = {
    "DUPLICATE_LOGIN": "Этот логин уже используется",
    "MISSING_DATA_COURIER": "Недостаточно данных для создания учетной записи",
    "MISSING_LOGIN_OR_PASSWORD": "Недостаточно данных для входа",
    "ACCOUNT_NOT_FOUND": "Учетная запись не найдена"
}

# --- Ожидаемые успешные ответы ---
EXPECTED_RESPONSES = {
    "CREATE_COURIER_SUCCESS": {"ok": True},
    "GET_ORDERS_LIST_SUCCESS": {"orders": list} 
}

# --- Готовые функции для получения уникальных данных ---
def get_unique_courier_data():
    """Возвращает словарь с уникальными данными курьера."""
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

def get_unique_order_data():
    """Возвращает словарь с уникальными данными заказа."""
    return {
        "firstName": generate_random_string(5),
        "lastName": generate_random_string(6),
        "address": f"{generate_random_string(10)}, apt. {generate_random_string(3)}",
        "metroStation": 4,
        "phone": f"+7 {generate_random_string(3)} {generate_random_string(3)} {generate_random_string(2)} {generate_random_string(2)}",
        "rentTime": 5,
        "deliveryDate": "2025-12-06",
        "comment": f"Test comment: {generate_random_string(10)}"
    }

# --- Готовые полезные нагрузки (payloads) с пропущенными полями ---
def get_courier_payload_without_login():
    """Возвращает payload для создания курьера без логина."""
    data = get_unique_courier_data()
    del data["login"]
    return data

def get_courier_payload_without_password():
    """Возвращает payload для создания курьера без пароля."""
    data = get_unique_courier_data()
    del data["password"]
    return data

def get_courier_payload_without_first_name():
    """Возвращает payload для создания курьера без firstName."""
    data = get_unique_courier_data()
    del data["firstName"]
    return data

# --- Данные для тестов создания заказа ---
# Цвета для параметризации
ORDER_COLORS = [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    []  # Без цвета
]

# Шаблон успешного ответа на создание заказа (для проверки ключей)
CREATE_ORDER_RESPONSE_SCHEMA = {"track": int}
