from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from chats.views import ChatView, HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("chat/", ChatView.as_view(), name="chat"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
