FROM python:3.12.3-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ ./src/

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/src

# Команда для запуска приложения
CMD ["python", "src/app.py"]
