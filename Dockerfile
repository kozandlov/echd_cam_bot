# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения и список зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Указываем команду запуска (замените на вашу, если отличается)
CMD ["python", "bot.py"]
