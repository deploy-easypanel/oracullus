#!/bin/sh
echo "Esperando pelo Postgres..."
until nc -z -v -w30 db 5432
do
  echo "Postgres não está pronto, esperando..."
  sleep 1
done

echo "Banco pronto! Rodando collectstatic..."
python manage.py collectstatic --noinput

echo "Aplicando migrations..."
python manage.py migrate

echo "Iniciando Gunicorn..."
exec "$@"
