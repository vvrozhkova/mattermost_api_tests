import string
import random
import requests
import allure
from allure_commons._allure import step
from utils.common_steps import assert_status_code, assert_response_param

team_id = "ktfw3dx11fradfpmsc3cekdrae"
channel_id = "q8ca1kujb7no8xw1aozhrmyj6h"
headers = {"Authorization": "Bearer ninp4h45ej8nzd6p4wjeo5hn7w"}

@allure.feature('Управление пользователями')
@allure.title('Добавление пользователя в канал')
def test_add_member(base_url):
    user_id = add_user(base_url)
    add_user_to_team(base_url, user_id)
    response = add_user_to_channel(base_url, user_id)
    assert response.json()["user_id"] == user_id

@allure.feature('Управление пользователями')
@allure.title('Удаление пользователя из канала')
def test_remove_member(base_url):
    user_id = add_user(base_url)
    add_user_to_team(base_url, user_id)
    add_user_to_channel(base_url, user_id)
    with allure.step('Выполняем запрос на удаление пользователя из команды'):
        response = requests.delete(f'{base_url}/channels/{channel_id}/members/{user_id}', headers=headers)
    assert_status_code(response, 200)
    assert_response_param(response, "status", "OK")


def generate_random_strings(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


@step("Добавляем пользователя")
def add_user(base_url):
    body = {"email": generate_random_strings(4) + "@" + generate_random_strings(4) + ".com",
            "username": generate_random_strings(4), "password": generate_random_strings(8)}
    with allure.step('Выполняем запрос на создание пользователя'):
        response = requests.post(f'{base_url}/users', json=body, headers=headers)
    assert_status_code(response, 201)
    return response.json()["id"]


@step("Добавляем пользователя в команду")
def add_user_to_team(base_url, user_id):
    body = {"user_id": user_id, "team_id": team_id}
    with allure.step('Выполняем запрос на добавление пользователя в команду'):
        response = requests.post(f'{base_url}/teams/{team_id}/members', json=body,
                                 headers=headers)
    assert_status_code(response, 201)

@step("Добавляем пользователя в канал")
def add_user_to_channel(base_url, user_id):
    body = {"user_id": user_id}
    response = requests.post(f'{base_url}/channels/{channel_id}/members', json=body,
                                   headers=headers)
    assert_status_code(response, 201)
    return response
