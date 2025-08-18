# Imagem base com Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Expõe a porta do Django
EXPOSE 8334

# Comando padrão para rodar o servidor de desenvolvimento
CMD ["python", "manage.py", "runserver", "0.0.0.0:8334"]
