# Используем базовый образ с Python
FROM python:3.11-slim

# Устанавливаем системные зависимости для сборки (если они нужны)
RUN apt-get update && apt-get install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем pip и setuptools (если их нет в образе)
RUN pip install --upgrade pip setuptools wheel numpy build


# Копируем исходный код проекта в контейнер
COPY ./ /app

# Переходим в директорию проекта
WORKDIR /app


# Собираем .whl файл
RUN python3 -m build

# Устанавливаем сгенерированный .whl файл
RUN pip install dist/TraceOfMatrix-*.whl


# Команда по умолчанию для выполнения скрипта
CMD ["python3", "perf.py"]
