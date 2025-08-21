import uuid

import requests
from decouple import config

from chats.models import ChatSession, Message

from .prompts import prompt
from .utils import md_answer

OLLAMA_URL = config("OLLAMA_URL")
MODEL_NAME = config("MODEL_NAME")


def process_user_message(question: str) -> None:
    chat_session, _ = ChatSession.objects.get_or_create(
        defaults={"id": uuid.uuid4()},
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)
    data = response.json()

    if "message" in data and "content" in data["message"]:
        answer = md_answer(data["message"]["content"])

    Message.objects.create(question=question, response=answer, session=chat_session)
