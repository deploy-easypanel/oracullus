import json

import requests
from decouple import config

from chats.models import ChatSession, Message

from .prompts import prompt
from .utils import md_answer

OLLAMA_URL = config("OLLAMA_URL")  # ex: http://apps_ollama:11434/completions
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

        # Requisição para a LLM
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)

        try:
            data = response.json()  # tenta decodificar JSON normalmente
        except json.JSONDecodeError:
            # fallback: pega só a primeira linha, evitando erro "Extra data"
            first_line = response.text.strip().split("\n")[0]
            data = json.loads(first_line)

        # Extrai a resposta
        answer = "Não foi possível gerar a resposta."
        if "message" in data and "content" in data["message"]:
            answer = md_answer(data["message"]["content"])

        # Salva no banco
        Message.objects.create(session=chat_session, question=question, response=answer)

    except requests.exceptions.Timeout:
        Message.objects.create(
            session=chat_session,
            question=question,
            response="Erro: A LLM demorou muito para responder (timeout).",
        )
    except requests.exceptions.ConnectionError:
        Message.objects.create(
            session=chat_session,
            question=question,
            response="Erro: Não foi possível conectar ao Ollama. Verifique o container.",
        )
    except Exception as e:
        Message.objects.create(
            session=chat_session,
            question=question,
            response=f"Erro ao processar a LLM: {str(e)}",
        )
