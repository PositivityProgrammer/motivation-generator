# Этап сборки и тестирования
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

# Запускаем тесты и сохраняем результаты
RUN pytest --cov=src --cov-report=xml:/app/coverage.xml tests/

# Этап для сохранения результатов тестов
FROM scratch as test-results
COPY --from=builder /app/coverage.xml .

# Этап создания финального образа
FROM python:3.12.3-slim

WORKDIR /app

# Копируем только необходимые файлы из этапа сборки
COPY --from=builder /app/src ./src
COPY --from=builder /app/requirements.txt .

# Устанавливаем только production-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/src

# Команда для запуска приложения
CMD ["python", "src/app.py"]
