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

# Copia dependências primeiro (cache eficiente)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copia o projeto
COPY . .

# Exponha a porta usada pelo Gunicorn
EXPOSE 8334

# Comando padrão para rodar com Gunicorn
CMD ["gunicorn", "setup.wsgi:application", "--bind", "0.0.0.0:8334", "--workers", "3"]
