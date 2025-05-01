from urls import COURIER_LOGIN_URL, COURIER_DELETE_URL
from random_data import *
import requests
import allure


@allure.feature("Courier")
@allure.story("Create courier")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    @allure.description("""
     Генерируем уникальный логин/пароль через вспомогательную функцию,
     отправляем POST /courier и ожидаем 201 + {"ok": true}.
     """)
    def test_create_courier_successfully(self):
        payload = return_random_login_password()
        response = requests.post(COURIER_CREATE_URL, json=payload)

        assert response.status_code == 201 and response.json() == {"ok": True}

        # Удаление созданного курьера
        response_login = requests.post(COURIER_LOGIN_URL, json=payload)
        assert response_login.status_code == 200
        courier_id = response_login.json().get("id")

        response_delete = requests.delete(f"{COURIER_DELETE_URL}/{courier_id}")
        assert response_delete.status_code == 200 and response_delete.json() == {"ok": True}

    @allure.title("Ошибка при попытке создать дубликат курьера")
    @allure.description("""
    Сначала создаём курьера, затем повторный POST /courier с тем же логином
    должен вернуть 409 и сообщение «Этот логин уже используется».
    """)
    def test_create_two_same_couriers_error(self):
        login_data = register_new_courier_and_return_login_password()
        response = requests.post(COURIER_CREATE_URL, json={
            "login": login_data[0],
            "password": login_data[1]
        })

        assert response.status_code == 409 and response.json() == {"message": "Этот логин уже используется"}

        # Удаление созданного курьера
        response_login = requests.post(COURIER_LOGIN_URL, json={
            "login": login_data[0],
            "password": login_data[1]
        })
        assert response_login.status_code == 200
        courier_id = response_login.json().get("id")

        response_delete = requests.delete(f"{COURIER_DELETE_URL}/{courier_id}")
        assert response_delete.status_code == 200 and response_delete.json() == {"ok": True}

    @allure.title("Ошибка при отсутствии обязательного поля")
    @allure.description("Отправляем POST /courier без поля login и ожидаем 400 + сообщение об ошибке.")
    def test_create_courier_with_no_required_field_error(self):
        response = requests.post(COURIER_CREATE_URL, data={
            "password": "1234",
            "firstName": "saske"
        })
        assert response.status_code == 400 and response.json() == {"message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Ошибка при создании курьера с уже существующим логином")
    @allure.description("Используем занятый логин ninja, ожидаем 409 + сообщение «Этот логин уже используется».")
    def test_create_courier_with_existing_login_error(self):
        response = requests.post(COURIER_CREATE_URL, json={
            "login": "ninja",
            "password": "1234"
        })
        assert response.status_code == 409 and response.json() == {"message": "Этот логин уже используется"}