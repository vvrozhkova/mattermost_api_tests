import allure
import pytest
import requests
from allure_commons._allure import step

@allure.feature('Аутентификация')
@allure.story('Успешная аутентификация')
@allure.title('Корректный логин и пароль')
def test_auth_success(base_url):
    """
        Тест для проверки успешной аутентификации пользователя с использованием
        корректных учетных данных

        1. Отправить login запрос, передав в теле корректные данные для авторизации
        2. Проверить статус код ответа = 200
        3. Проверить что в ответе вернулись данные авторизованного пользователя
        """
    body = {"login_id":"mm_test","password":"mm_pswd1","token":"","deviceId":""}
    response = login(base_url, body)
    with allure.step('Проверяем успешный ответ'):
        assert response.status_code == 200
        assert response.json()["email"] == "test@test.com"

@allure.feature('Аутентификация')
@allure.story('Неуспешная аутентификация')
@allure.title('Некорректный логин и пароль')
def test_wrong_login_and_pswd(base_url):
    """
       Тест для проверки неуспешной аутентификации пользователя с использованием
       некорректных учетных данных

       1. Отправить login запрос, передав в теле некорректные данные для авторизации, пользователя с таким login_id и password нет в БД
       2. Проверить статус код ответа = 401
       3. Проверить что в ответе вернулось корректное сообщение об ошибке
       """
    body = {"login_id":"mm_test12","password":"mm_pswd134","token":"","deviceId":""}
    response = login(base_url, body)
    with allure.step('Проверяем неуспешный ответ и сообщение об ошибке'):
        assert response.status_code == 401
        assert response.json()["message"] == "Enter a valid email or username and/or password."

@allure.feature('Аутентификация')
@allure.story('Неуспешная аутентификация')
@allure.title('Заблокированная учетная запись')
def test_block_user_login(base_url):
    """
       Тест для проверки неуспешной аутентификации пользователя который был заблокирован

       1. Отправить login запрос, передав в теле корректные данные для авторизации, но
       пользователь с таким login_id и password был заблокирован(параметр delete_at>0)
       2. Проверить статус код ответа = 401
       3. Проверить что в ответе вернулось корректное сообщение об ошибке
       """
    body = { "email": "blockuser@test.com", "username": "block_user","password": "block1234"}
    response = login(base_url, body)
    with allure.step('Проверяем неуспешный ответ и сообщение об ошибке'):
        assert response.status_code == 401
        assert response.json()["message"] == "Enter a valid email or username and/or password."

@allure.feature('Аутентификация')
@allure.story('Неуспешная аутентификация')
@allure.title('Не активированная учетная запись')
def test_not_activated_user_login(base_url):
    """
       Тест для проверки неуспешной аутентификации пользователя который не был активирован

       1. Отправить login запрос, передав в теле корректные данные для авторизации,
       пользователь с таким login_id и password не был активирован(параметр create_at==update_at)
       2. Проверить статус код ответа = 401
       3. Проверить что в ответе вернулось корректное сообщение об ошибке
       """
    body = {"email": "notactivateduser@test.com", "username": "not_activated_user", "password": "notactivated1234"}
    response = login(base_url, body)
    with allure.step('Проверяем неуспешный ответ и сообщение об ошибке'):
        assert response.status_code == 401
        assert response.json()["message"] == "Enter a valid email or username and/or password."

@allure.feature('Аутентификация')
@allure.story('Неуспешная аутентификация')
@allure.title('Отсутствие соединения с сервером')
def test_unable_server_connection(base_url):
    """
      Тест для проверки ошибки при отсутствии соединения с сервером

      1. Установить таймаут ответа на запрос на значение за которое сервер не успевает ответить, например 0.01
      2. Отправить login запрос, передав в теле корректные данные для авторизации
      2. Проверить полученное исключение
      """
    body = {"login_id":"mm_test","password":"mm_pswd1","token":"","deviceId":""}
    with allure.step('Отправляем запрос на авторизацию с таймаутом и проверяем исключение по таймауту'):
        with pytest.raises(requests.Timeout):
            requests.post(f'{base_url}/users/login', json=body, timeout=0.01)


@step("Отправляем запрос на авторизацию")
def login(base_url, body):
    return requests.post(f'{base_url}/users/login', json=body)
