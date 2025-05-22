# Используем официальный образ Python
FROM python:3.13-slim

FROM python:3.11-slim

# Устанавливаем необходимые системные библиотеки
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Запускаем скрипт
CMD ["python", "bot.py"]
