from urls import COURIER_CREATE_URL
import requests
import random
import string

# Генерация данных и создание курьера
def register_new_courier_and_return_login_password():

    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": ""
    }

    response = requests.post(COURIER_CREATE_URL, json=payload)

    if response.status_code == 201 and response.json() == {"ok": True}:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

# Генерация данных (без создания курьера) и их возвращение в формате payload
def return_random_login_password():

    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login = generate_random_string(10)
    password = generate_random_string(10)

    payload = {
        "login": login,
        "password": password
    }

    return payload