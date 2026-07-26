FROM python:3.11-slim

WORKDIR /app

# Установка системных пакетов (gcc, libpq-dev, netcat-openbsd)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Скрипт точки входа
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
