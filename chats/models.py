from django.db import models


class Chat(models.Model):
    question = models.CharField(
        verbose_name="Pergunta", max_length=255, null=False, blank=False
    )
    response = models.TextField(verbose_name="Resposta", null=False, blank=False)
    created_at = models.DateTimeField(
        verbose_name="Criado em", auto_now_add=True, null=False, blank=False
    )
