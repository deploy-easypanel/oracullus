# Imagem base com Python
FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git build-essential libfreetype6-dev \
        libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia dependências primeiro (para cache eficiente)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copia o projeto
COPY . .

# Exponha a porta usada pelo Gunicorn
EXPOSE 8334

# Variável de ambiente para usar settings de produção
ENV DJANGO_SETTINGS_MODULE=setup.settings.production

# Comando padrão para rodar com Gunicorn
# (substitua "setup" pelo nome do seu projeto onde fica o wsgi.py)
CMD ["gunicorn", "setup.wsgi:application", "--bind", "0.0.0.0:8334", "--workers", "3"]
