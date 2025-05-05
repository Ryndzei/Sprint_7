from data import payload_with_no_required_field, payload_with_existing_login
from random_data import return_random_login_password
from urls import COURIER_CREATE_URL
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
    def test_create_courier_successfully(self, courier_cleanup):
        payload = return_random_login_password()
        courier_cleanup.update(payload)

        with (allure.step("Отправляем POST /courier")):
            response = requests.post(COURIER_CREATE_URL, json=payload)

            assert response.status_code == 201, "Код ответа не 201"
            assert response.json() == {"ok": True}, "Тело ответа не соответствует строго ожидаемому"

    @allure.title("Ошибка при попытке создать дубликат курьера")
    @allure.description("""
    Сначала создаём курьера, затем повторный POST /courier с тем же логином
    должен вернуть 409 и сообщение «Этот логин уже используется».
    """)
    def test_create_two_same_couriers_error(self, courier_cleanup):
        payload = return_random_login_password()
        courier_cleanup.update(payload)

        with (allure.step("Отправляем первый POST /courier")):
            response_create = requests.post(COURIER_CREATE_URL, json=payload)
            assert response_create.status_code == 201 and response_create.json() == {"ok": True}

        with (allure.step("Пробуем отправить второй POST /courier с телом как у первого")):
            response_error = requests.post(COURIER_CREATE_URL, json=payload)

            assert response_error.status_code == 409, "Код ответа не 409"
            assert response_error.json() == {"message": "Этот логин уже используется"}, "Тело ответа не соответствует строго ожидаемому"

    @allure.title("Ошибка при отсутствии обязательного поля")
    @allure.description("Отправляем POST /courier без поля login и ожидаем 400 + сообщение об ошибке.")
    def test_create_courier_with_no_required_field_error(self):

        with (allure.step("Отправляем POST /courier с телом без обязательного поля login")):
            response = requests.post(COURIER_CREATE_URL, json=payload_with_no_required_field)

            assert response.status_code == 400, "Код ответа не 400"
            assert response.json() == {"message": "Недостаточно данных для создания учетной записи"}, "Тело ответа не соответствует строго ожидаемому"

    @allure.title("Ошибка при создании курьера с уже существующим логином")
    @allure.description("Используем занятый логин ninja, ожидаем 409 + сообщение «Этот логин уже используется».")
    def test_create_courier_with_existing_login_error(self):

        with (allure.step("Отправляем POST /courier с уже существующим в БД логином")):
            response = requests.post(COURIER_CREATE_URL, json=payload_with_existing_login)

            assert response.status_code == 409, "Код ответа не 409"
            assert response.json() == {"message": "Этот логин уже используется"}, "Тело ответа не соответствует строго ожидаемому"