#!/bin/sh
set -e

# Ожидаем, пока PostgreSQL запустится
echo "Waiting for PostgreSQL to start..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done
echo "PostgreSQL started."

# Выполняем миграции
python manage.py migrate

# Собираем статику
python manage.py collectstatic --noinput

exec "$@"
