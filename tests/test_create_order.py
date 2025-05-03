from data import order_payload_with_no_color_field
from urls import ORDER_CREATE_URL
import requests
import pytest
import allure


@allure.feature("Orders")
@allure.story("Create order")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами поля color")
    @allure.description("""
    Проверяем, что можно передать:
      • один цвет BLACK;
      • один цвет GREY;
      • оба цвета сразу
    Везде ожидаем 201 + в теле ключ track.
    """)
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    def test_create_order_color_field(self, color):
        payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": color
        }

        with (allure.step(f"Отправляем POST /orders для создания заказа с 'color': {color}")):
            response = requests.post(ORDER_CREATE_URL, json=payload)
            track_id = response.json().get("track")

            assert response.status_code == 201, "Код ответа не 201"
            assert response.json() == {"track": track_id}, "Тело ответа не соответствует строго ожидаемому"

    @allure.title("Создание заказа без поля color")
    @allure.description("Проверяем, что можно создать заказ без необязательного поля color")
    def test_create_order_with_no_color_field(self):

        with (allure.step(f"Отправляем POST /orders для создания заказа без поля color")):
            response = requests.post(ORDER_CREATE_URL, json=order_payload_with_no_color_field)
            track_id = response.json().get("track")

            assert response.status_code == 201, "Код ответа не 201"
            assert response.json() == {"track": track_id}, "Тело ответа не соответствует строго ожидаемому"