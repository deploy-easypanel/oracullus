from django.urls import path

from .views import ChatView, HomeView, chat_json

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("chat/", ChatView.as_view(), name="chat"),
    path("chat/json/<uuid:session_id>/", chat_json, name="chat_json"),
]
