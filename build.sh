#!/usr/bin/env bash
# exit on error
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Создаем директорию для статических файлов
mkdir -p staticfiles

# Добавляем .env в корень проекта
cp .env pricecalc/.env

# Проверка на наличие исправленного файла настроек
if [ -f "pricecalc/pricecalc/updated_settings.py" ]; then
  echo "Применяем исправленные настройки..."
  mv pricecalc/pricecalc/updated_settings.py pricecalc/pricecalc/settings.py
fi

# Создаем символическую ссылку на calculator внутри pricecalc/
if [ -d "calculator" ] && [ ! -d "pricecalc/calculator" ]; then
  echo "Создание символической ссылки на calculator..."
  ln -sf "$(pwd)/calculator" "$(pwd)/pricecalc/calculator"
fi

# Создаем файл __init__.py в директории, если его нет
touch calculator/__init__.py

# Добавляем wsgi.py в директорию pricecalc, если его нет
if [ ! -f "pricecalc/wsgi.py" ] && [ -f "pricecalc/pricecalc/wsgi.py" ]; then
  echo "Копируем wsgi.py в корневую директорию pricecalc..."
  cp pricecalc/pricecalc/wsgi.py pricecalc/wsgi.py
fi

# Миграции базы данных и статика
cd pricecalc
python manage.py migrate
python manage.py collectstatic --no-input --clear 