from threading import Thread

from django.shortcuts import redirect, render
from django.views.generic import View

from core.services import process_user_message

from .models import Message


def background_process(question):
    try:
        # Chama a função que já salva a resposta no banco
        process_user_message(question)
    except Exception as e:
        # Se der erro, salva mensagem de erro no banco
        Message.objects.create(user="LLM", content=f"Erro: {str(e)}")


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class ChatView(View):
    def get(self, request):
        messages = Message.objects.order_by("-created_at")
        return render(request, "chats/chat.html", {"messages": messages})

    def post(self, request):
        question = request.POST.get("message")
        if question:
            # Salva pergunta imediatamente com placeholder
            Message.objects.create(user="Você", content=question)
            # Processa a LLM em background
            thread = Thread(target=background_process, args=(question,))
            thread.start()
        return redirect("chat")
