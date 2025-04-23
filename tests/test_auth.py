import allure
import requests
from allure_commons._allure import step

@allure.feature('Аутентификация')
@allure.story('Успешная аутентификация')
@allure.title('Корректный логин и пароль')
def test_auth_success(base_url):
    body = {"login_id":"mm_test","password":"mm_pswd1","token":"","deviceId":""}
    response = login(base_url, body)
    with allure.step('Проверяем успешный ответ'):
        assert response.status_code == 200
        assert response.json()["email"] == "test@test.com"

@allure.feature('Аутентификация')
@allure.story('Неуспешная аутентификация')
@allure.title('Некорректный логин и пароль')
def test_wrong_login_and_pswd(base_url):
    body = {"login_id":"mm_test12","password":"mm_pswd134","token":"","deviceId":""}
    response = login(base_url, body)
    with allure.step('Проверяем неуспешный ответ и сообщение об ошибке'):
        assert response.status_code == 401
        assert response.json()["message"] == "Enter a valid email or username and/or password."

@allure.feature('Аутентификация')
@allure.story('Неуспешная аутентификация')
@allure.title('Заблокированная учетная запись')
def test_block_user_login(base_url):
    body = { "email": "blockuser@test.com", "username": "block_user","password": "block1234"}
    response = login(base_url, body)
    with allure.step('Проверяем неуспешный ответ и сообщение об ошибке'):
        assert response.status_code == 401
        assert response.json()["message"] == "Enter a valid email or username and/or password."

@allure.feature('Аутентификация')
@allure.story('Неуспешная аутентификация')
@allure.title('Не активированная учетная запись')
def test_not_activated_user_login(base_url):
    body = {"email": "notactivateduser@test.com", "username": "not_activated_user", "password": "notactivated1234"}
    response = login(base_url, body)
    with allure.step('Проверяем неуспешный ответ и сообщение об ошибке'):
        assert response.status_code == 401
        assert response.json()["message"] == "Enter a valid email or username and/or password."

@allure.feature('Аутентификация')
@allure.story('Неуспешная аутентификация')
@allure.title('Отсутствие соединения с сервером')
def test_unable_server_connection(base_url):
    body = {"login_id":"mm_test","password":"mm_pswd1","token":"","deviceId":""}
    with allure.step('Отправляем запрос на авторизацию с таймаутом'):
        requests.post(f'{base_url}/users/login', json=body, timeout=0.01)

@step("Отправляем запрос на авторизацию")
def login(base_url, body):
    return requests.post(f'{base_url}/users/login', json=body)
