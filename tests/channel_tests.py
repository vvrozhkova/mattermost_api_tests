import uuid
import allure
import requests
from utils.common_steps import assert_status_code, assert_response_param
from allure_commons._allure import step

headers = {"Authorization": "Bearer ninp4h45ej8nzd6p4wjeo5hn7w"}

@allure.feature('Создание чата/канала')
@allure.title('Создание чата/канала')
def test_create_channel(base_url):
    body = {"team_id":"ktfw3dx11fradfpmsc3cekdrae","name":f'{uuid.uuid4()}',"display_name":"123", "type": "O"}
    response = create_channel(base_url, body)
    assert_status_code(response, 201)

@allure.feature('Создание чата/канала')
@allure.title('Создание чата/канала с уже существующим именем')
def test_create_duplicate_channel(base_url):
    body = {"team_id":"ktfw3dx11fradfpmsc3cekdrae","name":f'{uuid.uuid4()}',"display_name":"123", "type": "O"}
    response = create_channel(base_url, body)
    assert_status_code(response, 201)
    response2 = create_channel(base_url, body)
    assert_status_code(response2, 400)
    assert_response_param(response2, "message", "A channel with that name already exists on the same team.")

@step("Отправляем запрос на создание чата/канала")
def create_channel(base_url, body):
    return requests.post(f'{base_url}/channels', json=body, headers=headers)