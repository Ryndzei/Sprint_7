import random
import string


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