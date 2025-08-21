import uuid

from django.db import models


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, related_name="messages"
    )
    question = models.CharField(
        verbose_name="Pergunta", max_length=255, null=False, blank=False
    )
    response = models.TextField(verbose_name="Resposta", null=False, blank=False)
    created_at = models.DateTimeField(
        verbose_name="Criado em", auto_now_add=True, null=False, blank=False
    )
