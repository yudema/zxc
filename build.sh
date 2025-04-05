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

# Добавляем wsgi.py в директорию pricecalc, если его нет
if [ ! -f "pricecalc/wsgi.py" ]; then
  echo "Создаем wsgi.py в корневой директории pricecalc..."
  echo '"""
WSGI config for pricecalc project.
"""
import os
import sys
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_PATH)
PRICECALC_APP_PATH = os.path.join(BASE_PATH, "pricecalc")
if PRICECALC_APP_PATH not in sys.path:
    sys.path.insert(0, PRICECALC_APP_PATH)
from pricecalc.wsgi import application
' > pricecalc/wsgi.py
fi

# Показываем содержимое директорий для отладки
echo "Содержимое директории pricecalc:"
ls -la pricecalc/
echo "Содержимое директории pricecalc/pricecalc:"
ls -la pricecalc/pricecalc/

# Миграции базы данных и статика
cd pricecalc
python manage.py migrate
python manage.py collectstatic --no-input --clear 