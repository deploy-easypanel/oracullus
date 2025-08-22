import uuid
from threading import Thread

import requests
from decouple import config

from chats.models import ChatSession, Message

from .prompts import prompt
from .utils import md_answer

OLLAMA_URL = config("OLLAMA_URL")
MODEL_NAME = config("MODEL_NAME")


def background_process_user_message(question: str):
    try:
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

        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        data = response.json()

        answer = "Não foi possível gerar a resposta."
        if "message" in data and "content" in data["message"]:
            answer = md_answer(data["message"]["content"])

        Message.objects.create(question=question, response=answer, session=chat_session)

    except Exception as e:
        Message.objects.create(
            question=question,
            response=f"Erro ao processar a LLM: {str(e)}",
            session=chat_session,
        )


def process_user_message_async(question: str):
    # Salva a pergunta imediatamente com resposta vazia
    chat_session, _ = ChatSession.objects.get_or_create(
        defaults={"id": uuid.uuid4()},
    )
    Message.objects.create(
        question=question, response="Processando...", session=chat_session
    )

    # Executa a LLM em background
    thread = Thread(target=background_process_user_message, args=(question,))
    thread.start()
