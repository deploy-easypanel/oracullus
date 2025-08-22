import requests
from decouple import config

from chats.models import ChatSession, Message

from .prompts import prompt
from .utils import md_answer

OLLAMA_URL = config("OLLAMA_URL")
MODEL_NAME = config("MODEL_NAME")


def process_user_message(question: str, session_id: str):
    try:
        chat_session = ChatSession.objects.get(id=session_id)

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

        Message.objects.create(session=chat_session, question=question, response=answer)

    except Exception as e:
        Message.objects.create(
            session=chat_session,
            question=question,
            response=f"Erro ao processar a LLM: {str(e)}",
        )
