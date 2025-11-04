from http.client import responses

import allure
import pytest
import requests
import jsonschema
from tests.schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_to_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка данных заказа"):
            assert response_json['id'] == payload['id'], "id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "id питомца не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "количество в заказе не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус заказа не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
            assert response.json()["id"] == 1

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self):

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_shop(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)
