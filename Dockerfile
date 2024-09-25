FROM python:3.12.3-slim as builder

WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt requirements-dev.txt ./

# Устанавливаем зависимости, включая инструменты для разработки
RUN pip install --no-cache-dir -r requirements-dev.txt

# Копируем исходный код
COPY src/ .
COPY tests/ ./tests/

# Запускаем тесты
RUN pytest --cov=src tests/

# Этап создания production-образа
FROM python:3.12.3-slim

WORKDIR /app

# Копируем только необходимые файлы из этапа сборки
COPY --from=builder /app/src/ .
COPY --from=builder /app/requirements.txt .

# Устанавливаем только production-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска приложения
CMD ["python", "src/app.py"]
