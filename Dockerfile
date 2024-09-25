FROM python:3.12.3-slim as builder

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt requirements-dev.txt ./

# Устанавливаем все зависимости
RUN pip install --no-cache-dir -r requirements-dev.txt

# Копируем весь проект
COPY . .

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/src

# Этап создания финального образа
FROM python:3.12.3-slim

WORKDIR /app

# Копируем файлы из этапа сборки
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/src

# Команда для запуска приложения
CMD ["python", "src/app.py"]
