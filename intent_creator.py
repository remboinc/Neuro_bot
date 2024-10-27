import os
import json
import requests
from dotenv import load_dotenv


def create_intent(project_id, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'x-goog-user-project': project_id,
        'Content-Type': 'application/json; charset=utf-8',
    }
    with open("questions.json", "r", encoding='utf-8') as file:
        intents_data = json.load(file)

    for intent_name, intent_data in intents_data.items():
        training_phrases = [
            {"parts": [{"text": question}]} for question in intent_data["questions"]
        ]

        body = {
            "displayName": intent_name,
            "trainingPhrases": training_phrases,
            "messages": [
                {
                    "text": {
                        "text": [intent_data["answer"]]
                    }
                }
            ]
        }
        endpoint = f'https://dialogflow.googleapis.com/v2/projects/{project_id}/agent/intents'
        response = requests.post(
            endpoint,
            json=body,
            headers=headers
        )
        response.raise_for_status()

        return intent_name


if __name__ == '__main__':
    load_dotenv()
    project_id = os.getenv('PROJECT_ID')
    gcloud_access_token = os.getenv("GCLOUD_ACCESS_TOKEN")
    try:
        intent_name = create_intent(project_id, gcloud_access_token)
        print(f"Интент '{intent_name}' успешно создан.")
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка при создании интента: {e}")


