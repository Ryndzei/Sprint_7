from urls import ORDERS_GET_LIST_URL
import requests
import allure

@allure.feature("Orders")
@allure.story("List orders")
class TestOrdersList:

    @allure.title("Успешное получение списка заказов")
    @allure.description("Отправляем GET /orders и проверяем, что в ответе есть ключ orders со списком заказов.")
    def test_get_list_of_orders_successfully(self):
        response = requests.get(ORDERS_GET_LIST_URL)
        body = response.json()

        assert "orders" in body and isinstance(body["orders"], list)