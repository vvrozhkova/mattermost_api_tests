import allure
import requests
from allure_commons._allure import step

from utils.common_steps import assert_status_code, assert_response_param

headers = {"Authorization": "Bearer ninp4h45ej8nzd6p4wjeo5hn7w"}
channel_id = "q8ca1kujb7no8xw1aozhrmyj6h"


@allure.feature('Отправка сообщения')
@allure.title('Проверка отправки сообщения в чат')
def test_create_message(base_url):
    """
     Тест для проверки отправки сообщения в чат

     1. Отправить POST /posts запрос, передав в теле данные с параметрами channel_id, message
     2. Проверить статус код ответа = 201 и что в теле ответа вернулись данные пользователя который добавил сообщение
     """
    body = {"channel_id": channel_id, "message": "string"}
    with allure.step('Выполняем запрос на отправку сообщения в чат'):
        response = requests.post(f'{base_url}/posts', json=body, headers=headers)
    assert_status_code(response, 201)
    assert_response_param(response, "user_id", '5tn53iqi87bcufo4jsh34u1o8c')
    channel_messages = get_channel_messages(base_url, channel_id)
    message_is_added_to_channel = channel_messages[response.json()["id"]]
    assert message_is_added_to_channel


@allure.feature('Отправка сообщения')
@allure.title('Проверка получения сообщения в чате')
def test_get_channel_messages(base_url):
    """
     Тест для проверки получения сообщения в чате

     1. Отправить GET /channels/{channel_id}/posts запрос, где channel_id = id канала
     2. Проверить статус код ответа = 200 и что в теле ответа вернулся не пустой список posts
     """
    channel_messages = get_channel_messages(base_url, channel_id)
    with allure.step('Проверка, что список сообщений не пустой'):
        assert channel_messages


@step("Получаем сообщения из канала")
def get_channel_messages(base_url, channel_id):
    with allure.step('Выполняем запрос на получение сообщений из чата'):
        response = requests.get(f'{base_url}/channels/{channel_id}/posts', headers=headers)
    assert_status_code(response, 200)
    return response.json()["posts"]
