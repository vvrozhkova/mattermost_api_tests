from allure_commons._allure import step


@step("Проверяем код ответа {status_code}")
def assert_status_code(response, status_code):
    assert response.status_code == status_code


@step("Проверяем поле ответа {param}={value}")
def assert_response_param(response, param, value):
    assert response.json()[param] == value