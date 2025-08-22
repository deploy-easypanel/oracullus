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
        # Recupera ou cria a sessão de chat
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
        text = response.text.strip()

        # Se resposta estiver vazia
        if not text:
            answer = "Erro: A LLM não retornou resposta."
        else:
            try:
                data = json.loads(text)  # tenta decodificar JSON completo
            except json.JSONDecodeError:
                # fallback: tenta extrair o primeiro JSON válido
                first_brace = text.find("{")
                last_brace = text.rfind("}") + 1
                if first_brace != -1 and last_brace != -1:
                    json_text = text[first_brace:last_brace]
                    data = json.loads(json_text)
                else:
                    data = None

            # Extrai a resposta da LLM
            if data and "message" in data and "content" in data["message"]:
                answer = md_answer(data["message"]["content"])
            else:
                answer = "Erro: Não foi possível processar a resposta da LLM."

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
