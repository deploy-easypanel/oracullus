from decouple import config

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Banco local SQLite por padrão, mas pode usar PostgreSQL se quiser
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
