from django.shortcuts import redirect, render
from django.views.generic import View

from core.services import process_user_message

from .models import Message


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class ChatView(View):
    def get(self, request):
        messages = Message.objects.order_by("-created_at")
        return render(request, "chats/chat.html", {"messages": messages})

    def post(self, request):
        question = request.POST.get("message")
        process_user_message(question)
        return redirect("chat")
