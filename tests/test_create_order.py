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
      • оба цвета сразу;
      • тело без поля color
    Везде ожидаем 201 + в теле ключ track.
    """)
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"],  None])
    def test_color_field(self, color):
        payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        }

        if color is not None:
            payload["color"] = color

        response = requests.post(ORDER_CREATE_URL, json=payload)
        track_id = response.json().get("track")

        assert response.status_code == 201 and response.json() == {"track": track_id}