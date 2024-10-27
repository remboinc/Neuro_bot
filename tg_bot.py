import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from google.cloud import dialogflow


async def start(update: Update, context):
    await update.message.reply_text('Привет! Спроси меня что-нибудь, и я отвечу!')


async def process_user_message(update: Update, context):
    user_message = update.message.text
    session_id = f"tg-{update.message.from_user.id}"
    dialogflow_response = await detect_intent_from_dialogflow(user_message, session_id)
    await send_bot_response(update, dialogflow_response)


async def detect_intent_from_dialogflow(text, session_id):
    project_id = os.getenv('PROJECT_ID')
    if not project_id:
        logging.error("PROJECT_ID не задан.")

    session_client = dialogflow.SessionsClient()

    logging.info(f"Запрос к Dialogflow: text='{text}', session_id='{session_id}'")

    try:
        session = session_client.session_path(project_id, session_id)
        text_input = dialogflow.TextInput(text=text, language_code='ru')
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        fulfillment_text = response.query_result.fulfillment_text
        is_fallback = response.query_result.intent.is_fallback

        if is_fallback:
            logging.info(f"Fallback intent detected для сессии {session_id}")
            return None
        else:
            logging.info(f"Получен fulfillmentText: {fulfillment_text}")
            return fulfillment_text
    except Exception as e:
        logging.error(f"Ошибка при запросе к Dialogflow: {e}")
        return None


async def send_bot_response(update: Update, response):
    if response:
        try:
            logging.info(f"Отправка ответа пользователю: {response}")
            await update.message.reply_text(response)
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")
    else:
        logging.info("Ответ не получен или является fallback.")


def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not telegram_token:
        logging.error("TELEGRAM_BOT_TOKEN не задан.")

    app = Application.builder().token(telegram_token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_user_message))

    app.run_polling()


if __name__ == '__main__':
    main()
