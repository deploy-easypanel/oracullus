FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git build-essential libfreetype6-dev libpq-dev curl netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

# Copia todo o projeto
COPY . .

# Copia o entrypoint e torna executável
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Expõe a porta do Django
EXPOSE 8334

# Define variável de ambiente para produção
ENV DJANGO_SETTINGS_MODULE=setup.settings.production

# Comando padrão do container (Gunicorn)
CMD ["gunicorn", "setup.wsgi:application", "--bind", "0.0.0.0:8334", "--workers", "3"]
