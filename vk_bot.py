import logging
import os
import random

import requests
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

load_dotenv()


def echo(event, message, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000)
    )


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


if __name__ == "__main__":
    vk_session = vk.VkApi(token=os.getenv("VK_APP_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            session_id = event.user_id
            response_from_bot = detect_intent_from_dialogflow(event.text, session_id)
            echo(event, response_from_bot, vk_api)
