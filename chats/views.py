import uuid
from threading import Thread

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from chats.models import ChatSession, Message
from core.services import process_user_message


def background_process(question, session_id):
    process_user_message(question, session_id=session_id)


class HomeView(View):
    def get(self, request):
        return render(request, "chats/home.html")


class ChatView(View):
    def get(self, request):
        session, _ = ChatSession.objects.get_or_create(id=uuid.uuid4())
        messages = session.messages.order_by("created_at")
        return render(
            request, "chats/chat.html", {"messages": messages, "session_id": session.id}
        )

    def post(self, request):
        question = request.POST.get("message")
        session_id = request.POST.get("session_id")

        if not session_id:
            session = ChatSession.objects.create(id=uuid.uuid4())
            session_id = session.id

        Message.objects.create(
            session_id=session_id, question=question, response="Processando..."
        )

        thread = Thread(target=background_process, args=(question, session_id))
        thread.start()

        return redirect("chat")


def chat_json(request, session_id):
    session = ChatSession.objects.get(id=session_id)
    messages = session.messages.order_by("created_at").values("question", "response")
    return JsonResponse({"messages": list(messages)})
