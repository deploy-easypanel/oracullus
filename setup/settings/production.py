from decouple import Csv, config

from .base import *

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())
DEBUG = config("DEBUG", cast=bool, default=False)

# Banco de dados vindo do DATABASE_URL (Postgres geralmente)
DATABASES = {
    "default": db_url(
        default=config("DATABASE_URL"),
    )
}
