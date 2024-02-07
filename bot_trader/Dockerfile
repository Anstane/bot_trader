# Используем базовый образ Python 3.11 slim
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем poetry
RUN pip install poetry==1.6.1

# Копируем файлы для установки зависимостей
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости с помощью poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копируем все остальные файлы проекта в рабочую директорию контейнера
COPY . ./

# Команда для запуска бота
CMD ["python", "bot.py"]
