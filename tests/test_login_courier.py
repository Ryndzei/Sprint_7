from urls import COURIER_LOGIN_URL, COURIER_DELETE_URL
from random_data import register_new_courier_and_return_login_password
import requests
import allure


@allure.feature("Courier")
@allure.story("Login courier")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    @allure.description("""
    Регистрируем нового курьера, логинимся через POST /courier/login,
    ожидаем 200 + в теле ключ id (число).
    """)
    def test_login_courier_successfully(self):
        login_data = register_new_courier_and_return_login_password()
        response = requests.post(COURIER_LOGIN_URL, json={
            "login": login_data[0],
            "password": login_data[1]
        })
        courier_id = response.json().get("id")

        assert response.status_code == 200 and response.json() == {"id": courier_id}

        # Удаление созданного курьера
        response_delete = requests.delete(f"{COURIER_DELETE_URL}/{courier_id}")
        assert response_delete.status_code == 200 and response_delete.json() == {"ok": True}

    @allure.title("Ошибка при авторизации с неверными данными")
    @allure.description("POST /courier/login с неправильным паролем, ожидаем 404.")
    def test_login_courier_with_incorrect_or_inexisting_data_error(self):
        response = requests.post(COURIER_LOGIN_URL, json={
            "login": "ninja",
            "password": "1235"
        })

        assert response.status_code == 404 and response.json() == {"message": "Учетная запись не найдена"}

    @allure.title("Ошибка при авторизации без обязательных полей")
    @allure.description("POST /courier/login без поля login, ожидаем 400 + сообщение «Недостаточно данных для входа».")
    def test_login_courier_with_no_required_field_error(self):
        response = requests.post(COURIER_LOGIN_URL, json={
            "password": "1234"
        })

        assert response.status_code == 400 and response.json() == {"message":  "Недостаточно данных для входа"}