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

# Показываем содержимое директорий для отладки
echo "Содержимое директории pricecalc:"
ls -la pricecalc/
echo "Содержимое директории pricecalc/pricecalc:"
ls -la pricecalc/pricecalc/

# Создаем правильный wsgi.py
echo '"""
WSGI config for pricecalc project.
"""
import os
import sys

# Добавляем директории проекта в sys.path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_PATH)

# Настраиваем переменные окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricecalc.settings")

# Создаем WSGI приложение
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()' > pricecalc/wsgi.py

# Создаем urls.py для корня проекта с прямыми маршрутами, без импорта
echo '"""
URL configuration for root pricecalc project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect("calculator:index")

urlpatterns = [
    path("", home_redirect, name="home"),
    path("admin/", admin.site.urls),
    path("calculator/", include("calculator.urls")),
]' > pricecalc/urls.py

# Проверяем, что файлы созданы
echo "Проверяем, что файл wsgi.py создан:"
cat pricecalc/wsgi.py
echo "Проверяем, что файл urls.py создан:"
cat pricecalc/urls.py

# Миграции базы данных и статика
cd pricecalc
python manage.py migrate
python manage.py collectstatic --no-input --clear 