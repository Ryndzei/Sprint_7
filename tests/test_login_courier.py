from data import payload_with_wrong_pass, login_payload_with_no_required_field
from urls import COURIER_LOGIN_URL, COURIER_CREATE_URL
from random_data import return_random_login_password
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
    def test_login_courier_successfully(self, courier_cleanup):
        payload = return_random_login_password()
        courier_cleanup.update(payload)

        with (allure.step("Отправляем POST /courier для создания курьера")):
            response_create = requests.post(COURIER_CREATE_URL, json=payload)
            assert response_create.status_code == 201 and response_create.json() == {"ok": True}

        with (allure.step("Отправляем POST /courier/login для авторизации")):
            response_login = requests.post(COURIER_LOGIN_URL, json=payload)
            courier_id = response_login.json().get("id")

            assert response_login.status_code == 200, "Код ответа не 200"
            assert response_login.json() == {"id": courier_id}, "Тело ответа не соответствует строго ожидаемому"

    @allure.title("Ошибка при авторизации с неверными данными")
    @allure.description("POST /courier/login с неправильным паролем, ожидаем 404.")
    def test_login_courier_with_incorrect_or_inexisting_data_error(self):

        with (allure.step("Отправляем POST /courier/login с неверным паролем")):
            response = requests.post(COURIER_LOGIN_URL, json=payload_with_wrong_pass)

            assert response.status_code == 404, "Код ответа не 404"
            assert response.json() == {"message": "Учетная запись не найдена"}, "Тело ответа не соответствует строго ожидаемому"

    @allure.title("Ошибка при авторизации без обязательных полей")
    @allure.description("POST /courier/login без поля login, ожидаем 400 + сообщение «Недостаточно данных для входа».")
    def test_login_courier_with_no_required_field_error(self):

        with (allure.step("Отправляем POST /courier/login с телом без обязательного поля login")):
            response = requests.post(COURIER_LOGIN_URL, json=login_payload_with_no_required_field)

            assert response.status_code == 400, "Код ответа не 400"
            assert response.json() == {"message":  "Недостаточно данных для входа"}, "Тело ответа не соответствует строго ожидаемому"