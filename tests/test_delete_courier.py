from random_data import return_random_login_password
from urls import COURIER_CREATE_URL, COURIER_LOGIN_URL, COURIER_DELETE_URL
import requests
import allure


@allure.feature("Courier")
@allure.story("Delete courier")
class TestDeleteCourier:

    @allure.title("Успешное удаление курьера")
    @allure.description("""
        Регистрируем нового курьера, логинимся через POST /courier/login,
        удаляем курьера через DELETE /courier/:id
        ожидаем 200 + {'ok': True} в теле.
        """)
    def test_delete_courier_successfully(self):
        payload = return_random_login_password()

        with (allure.step("Отправляем POST /courier")):
            response_create = requests.post(COURIER_CREATE_URL, json=payload)
            assert response_create.status_code == 201 and response_create.json() == {"ok": True}

        with (allure.step("Отправляем POST /courier/login для получения ID")):
            response_login = requests.post(COURIER_LOGIN_URL, json=payload)
            courier_id = response_login.json().get("id")

        with (allure.step(f"Отправляем DELETE /courier/{courier_id}")):
            response_delete = requests.delete(COURIER_DELETE_URL + f"{courier_id}", json={"id": f"{courier_id}"})
            assert response_delete.status_code == 200, "Код ответа не 200"
            assert response_delete.json() == {'ok': True}, "Тело ответа не соответствует строго ожидаемому"

    @allure.title("Ошибка удаления курьера без id")
    @allure.description("""
            Удаляем курьера через DELETE /courier/ без id
            ожидаем 400 + {'message': 'Недостаточно данных для удаления курьера'} в теле.
            """)
    def test_delete_courier_with_no_id_error(self):

        with (allure.step(f"Отправляем DELETE /courier/ без id")):
            response_delete = requests.delete(COURIER_DELETE_URL)
            assert response_delete.status_code == 400, "Код ответа не 400"
            assert response_delete.json() == {"message":  "Недостаточно данных для удаления курьера"}, "Тело ответа не соответствует строго ожидаемому"

    @allure.title("Ошибка удаления курьера с несуществующим id")
    @allure.description("""
                Удаляем курьера через DELETE /courier/3 с несуществующим id 3
                ожидаем 404 + {'message': 'Курьера с таким id нет'} в теле.
                """)
    def test_delete_courier_with_inexisting_id_error(self):

        with (allure.step(f"Отправляем DELETE /courier/3 с несуществующим id 3")):
            response_delete = requests.delete(COURIER_DELETE_URL + "3", json={"id": "3"})
            assert response_delete.status_code == 404, "Код ответа не 400"
            assert response_delete.json() == {"message": "Курьера с таким id нет"}, "Тело ответа не соответствует строго ожидаемому"