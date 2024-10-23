# Боты для ответов на вопросы пользователей
Это два бота в Telegram и VK для ответов на самые популярные вопросы пользователей.
Используется библиотека dialogflow -- облачный сервис для распознавания естественного языка от Google.

![20241021020206489](https://github.com/user-attachments/assets/229b9eb7-aa7f-4a4d-83b2-4e001c166204)

# Как начать
Для запуска понадобится Python третьей версии.

Скачайте код с GitHub.
```commandline
git clone https://github.com/remboinc/Neuro_bot.git
```
Затем установите зависимости:
```commandline
pip install -r requirements.txt
```
Создайте файл .env, вставьте в него:
```commandline
TELEGRAM_BOT_TOKEN='токен вашего телеграм бота'
PROJECT_ID=neuro-bot-412345
VK_APP_TOKEN='токен вашей группы ВК'
GCLOUD_ACCESS_TOKEN='ваш google cloud token'
```
GCLOUD_ACCESS_TOKEN генерируется командой в терминале:
```commandline
gcloud auth application-default print-access-token
```

Как получить PROJECT_ID от https://dialogflow.cloud.google.com
Читайте в официальной документации

Примеры ботов:
- TG: @Neuro_for_people_bot
- VK: club227921191

## Зачем нужен скрипт intent_creator.py
Скрипт нужен, чтобы заносить возможные вопросы юзеров и ответы на них в dialogflow. Он парсит json файл [questions.json](questions.json) и отсылает POST запрос с готовыми интентами на сервер.
Пример работы скрипта

```text
Интент 'Устройство на работу' успешно создан.
Интент 'Забыл пароль' успешно создан.
Интент 'Удаление аккаунта' успешно создан.
Интент 'Вопросы от забаненных' успешно создан.
Интент 'Вопросы от действующих партнёров' успешно создан.

Process finished with exit code 0
```

