import uuid
import allure
import requests
from utils.common_steps import assert_status_code, assert_response_param
from allure_commons._allure import step

headers = {"Authorization": "Bearer ninp4h45ej8nzd6p4wjeo5hn7w"}


@allure.feature('Создание чата/канала')
@allure.title('Создание чата/канала')
def test_create_channel(base_url):
    """
      Тест для проверки создания чата/канала

      1. Отправить /channels запрос, передав в теле корректные данные для создания чата
      2. Проверить статус код ответа = 201
      """
    channel_name = f'{uuid.uuid4()}'
    body = {"team_id": "ktfw3dx11fradfpmsc3cekdrae", "name": channel_name, "display_name": "123", "type": "O"}
    response = create_channel(base_url, body)
    assert_status_code(response, 201)
    with allure.step('Проверяем что канал появился в списке каналов'):
        assert get_channels_by_name(base_url, channel_name)


@allure.feature('Создание чата/канала')
@allure.title('Создание чата/канала с уже существующим именем')
def test_create_duplicate_channel(base_url):
    """
      Тест для проверки создания чата/канала с уже существующим именем

      1. Отправить /channels запрос, передав в теле корректные данные для создания чата
      2. Проверить статус код ответа = 201
      3. Отправить /channels запрос, передав в теле такие же данные для создания чата как в шаге 1
      4. Проверить статус код ответа = 400 и текст сообщения "A channel with that name already exists on the same team."
      """
    channel_name = f'{uuid.uuid4()}'
    body = {"team_id": "ktfw3dx11fradfpmsc3cekdrae", "name": channel_name, "display_name": "123", "type": "O"}
    response = create_channel(base_url, body)
    assert_status_code(response, 201)
    with allure.step(f'Проверяем что количество каналов с именем {channel_name} равно 1'):
        assert len(get_channels_by_name(base_url, channel_name)) == 1
    response2 = create_channel(base_url, body)
    assert_status_code(response2, 400)
    assert_response_param(response2, "message", "A channel with that name already exists on the same team.")
    with allure.step(f'Проверяем что количество каналов с именем {channel_name} равно 1'):
        assert len(get_channels_by_name(base_url, channel_name)) == 1


def create_channel(base_url, body):
    with allure.step(f'Отправляем запрос на создание чата/канала {body["name"]}'):
        return requests.post(f'{base_url}/channels', json=body, headers=headers)


@step("Отправляем запрос на получение списка чатов/каналов")
def get_channels_by_name(base_url, channel_name):
    response = requests.get(f'{base_url}/channels', headers=headers)
    return [x for x in response.json() if x["name"] == channel_name]
