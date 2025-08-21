FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git build-essential libfreetype6-dev libpq-dev curl netcat && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8334
ENV DJANGO_SETTINGS_MODULE=setup.settings.production
CMD ["gunicorn", "setup.wsgi:application", "--bind", "0.0.0.0:8334", "--workers", "3"]
