import pytest
import requests
import allure
from urls import COURIER_LOGIN_URL, COURIER_DELETE_URL


@pytest.fixture
def courier_cleanup(request):

    payload = {}

    def fin():

        if payload:
            with allure.step("POST /courier/login — получаем ID для удаления"):
                response_login = requests.post(COURIER_LOGIN_URL, json=payload)
                assert response_login.status_code == 200
                courier_id = response_login.json()["id"]

            with allure.step(f"DELETE /courier/{courier_id} — удаляем курьера по полученному ID"):
                response_delete = requests.delete(f"{COURIER_DELETE_URL}/{courier_id}")
                assert response_delete.status_code == 200
                assert response_delete.json() == {"ok": True}

    request.addfinalizer(fin)

    return payload
