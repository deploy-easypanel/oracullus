from decouple import config

from .base import *

DEBUG = False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="oracullus.saulojustiniano.site,www.oracullus.saulojustiniano.site,saulojustiniano.site,www.saulojustiniano.site",
)

CSRF_TRUSTED_ORIGINS = [
    "https://oracullus.saulojustiniano.site",
    "https://www.oracullus.saulojustiniano.site",
    "https://saulojustiniano.site",
    "https://www.saulojustiniano.site",
]

# Segurança extra
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Banco de dados vindo do DATABASE_URL (Postgres geralmente)
DATABASES = {
    "default": db_url(
        default=config("DATABASE_URL"),
    )
}
