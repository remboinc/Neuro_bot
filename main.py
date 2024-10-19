import logging
import os
import requests
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()
os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


async def start(update: Update, context):
    await update.message.reply_text('Привет! Я эхо-бот. Напиши мне что-нибудь, и я повторю!')


async def echo(update: Update, context):
    user_message = update.message.text
    session_id = str(update.message.id)

    dialogflow_response = detect_intent_from_dialogflow(user_message, session_id)

    await update.message.reply_text(dialogflow_response)


def detect_intent_from_dialogflow(text, session_id):
    project_id = os.getenv('PROJECT_ID')
    gcloud_access_token = os.getenv("GCLOUD_ACCESS_TOKEN")

    url = f"https://dialogflow.googleapis.com/v2/projects/{project_id}/agent/sessions/{session_id}:detectIntent"

    headers = {
        'Authorization': 'Bearer ' + gcloud_access_token,
        'x-goog-user-project': project_id,
        'Content-Type': 'application/json; charset=utf-8',
    }


    data = {
        "queryInput": {
            "text": {
                "text": text,
                "languageCode": "ru"
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    logging.info(response.text)

    response_data = response.json()

    return response_data['queryResult']['fulfillmentText']


def main():
    app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  

    app.run_polling()


if __name__ == '__main__':
    main()