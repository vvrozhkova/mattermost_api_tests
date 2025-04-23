# Проект автотестов для проверки API взаимодествия с сервисом для обмена сообщениями Mattermost

### Локальный запуск автотестов

#### Выполнить в cli:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

#### Получение отчёта:
```bash
allure serve ./reports
```

### Allure отчет

#### Общие результаты
![allure_report_overview](pictures/1.png)

#### Шаги выполнения и список тестов
![allure_report_steps_and_cases](pictures/2.png)

#### Распределение по категориям
![allure_report_behaviors](pictures/3.png)
