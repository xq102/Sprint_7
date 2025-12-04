import requests
from config import BASE_URL, REQUEST_TIMEOUT


class CourierApi:
    @staticmethod
    def create_courier(payload):
        url = f"{BASE_URL}/courier"
        response = requests.post(url, data=payload, timeout=REQUEST_TIMEOUT)
        return response

    @staticmethod
    def login_courier(payload):
        url = f"{BASE_URL}/courier/login"
        response = requests.post(url, data=payload, timeout=REQUEST_TIMEOUT)
        return response

    @staticmethod
    def delete_courier(courier_id):
        if courier_id is not None:
            url = f"{BASE_URL}/courier/{courier_id}"
            response = requests.delete(url, timeout=REQUEST_TIMEOUT)
            return response
        return None

    @staticmethod
    def get_courier_id_by_login_pass(login, password):
        payload = {"login": login, "password": password}
        response = CourierApi.login_courier(payload)
        if response.status_code == 200:
            return response.json().get("id")
        return None


class OrderApi:
    @staticmethod
    def create_order(payload):
        url = f"{BASE_URL}/orders"
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        return response

    @staticmethod
    def get_orders_list():
        url = f"{BASE_URL}/orders"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        return response
    