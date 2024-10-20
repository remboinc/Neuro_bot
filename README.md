# Боты для ответов на вопросы пользователей
Это два бота в Telegram и VK для ответов на самые популярные вопросы пользователей.
Используется библиотека dialogflow -- облачный сервис для распознавания естественного языка от Google.

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
```

Как получить PROJECT_ID от https://dialogflow.cloud.google.com
Читайте в официальной документации

Примеры ботов:
TG: @Neuro_for_people_bot
VK: club227921191