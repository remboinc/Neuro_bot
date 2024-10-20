import logging
import os
import random

import requests
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_dialogflow_headers(project_id):
    gcloud_access_token = os.getenv("GCLOUD_ACCESS_TOKEN")

    headers = {
        'Authorization': 'Bearer ' + gcloud_access_token,
        'x-goog-user-project': project_id,
        'Content-Type': 'application/json; charset=utf-8',
    }
    return headers

def echo(event, message, vk_api):
    logging.info(f"Отправка сообщения пользователю {event.user_id}: {message}")
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000)
    )


def detect_intent_from_dialogflow(text, session_id, headers):
    logging.info(f"Запрос к Dialogflow: text='{text}', session_id='{session_id}'")

    url = f"https://dialogflow.googleapis.com/v2/projects/{project_id}/agent/sessions/{session_id}:detectIntent"

    data = {
        "queryInput": {
            "text": {
                "text": text,
                "languageCode": "ru"
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        logging.info(f"Ответ от Dialogflow: {response_data}")

        is_fallback = response_data['queryResult']['intent'].get('isFallback', False)
        if is_fallback:
            logging.info(f"Fallback intent detected для сессии {session_id}")
            return None
        else:
            fulfillment_text = response_data['queryResult']['fulfillmentText']
            logging.info(f"Получен fulfillmentText: {fulfillment_text}")
            return fulfillment_text

    except requests.exceptions.HTTPError as e:
        logging.error(f"Ошибка при запросе к Dialogflow: {e}")


if __name__ == "__main__":
    project_id = os.getenv('PROJECT_ID')
    headers = get_dialogflow_headers(project_id)
    vk_session = vk.VkApi(token=os.getenv("VK_APP_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logging.info("Бот запущен и готов к работе.")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logging.info(f"Новое сообщение от пользователя {event.user_id}: {event.text}")
            session_id = event.user_id
            response_from_bot = detect_intent_from_dialogflow(event.text, session_id, headers)
            if response_from_bot:
                logging.info(f"Отправка ответа пользователю {event.user_id}")
                echo(event, response_from_bot, vk_api)
            else:
                logging.info(f"Ответ пользователю {event.user_id} не отправлен (fallback intent)")