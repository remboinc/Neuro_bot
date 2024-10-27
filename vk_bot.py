import logging
import os
import random

import requests
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import dialogflow


def message_sender(event, message, vk_api):
    logging.info(f"Отправка сообщения пользователю {event.user_id}: {message}")
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000)
    )


def detect_intent_from_dialogflow(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    logging.info(f"Запрос к Dialogflow: text='{text}', session_id='{session_id}'")

    try:
        session = session_client.session_path(project_id, session_id)
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        logging.info(f"Ответ от Dialogflow: {response.query_result.fulfillment_text}")
        is_fallback = response.query_result.intent.is_fallback

        if is_fallback:
            logging.info(f"Fallback intent detected для сессии {session_id}")
            return None
        else:
            fulfillment_text = response.query_result.fulfillment_text
            logging.info(f"Получен fulfillmentText: {fulfillment_text}")
            return fulfillment_text

    except requests.exceptions.HTTPError as e:
        logging.error(f"Ошибка при запросе к Dialogflow: {e}")


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    project_id = os.getenv('PROJECT_ID')
    vk_session = vk.VkApi(token=os.getenv("VK_APP_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logging.info("Бот запущен и готов к работе.")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logging.info(f"Новое сообщение от пользователя {event.user_id}: {event.text}")
            session_id = f'vk_{event.user_id}'
            response_from_bot = detect_intent_from_dialogflow(project_id, session_id, event.text, language_code='ru')
            if response_from_bot:
                logging.info(f"Отправка ответа пользователю {session_id}")
                message_sender(event, response_from_bot, vk_api)
            else:
                logging.info(f"Ответ пользователю {session_id} не отправлен (fallback intent)")
