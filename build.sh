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

# Создаем или заменяем urls.py в pricecalc/pricecalc
echo '"""
URL configuration for pricecalc project.
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
]' > pricecalc/pricecalc/urls.py

# Добавляем простой файл wsgi.py (Django будет использовать свой wsgi)
if [ ! -f "pricecalc/pricecalc/wsgi.py" ]; then
  echo '"""
WSGI config for pricecalc project.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricecalc.settings")
application = get_wsgi_application()' > pricecalc/pricecalc/wsgi.py
fi

# Проверяем, что файлы созданы
echo "Файл urls.py создан:"
cat pricecalc/pricecalc/urls.py

# Миграции базы данных и статика
cd pricecalc
python manage.py migrate
python manage.py collectstatic --no-input --clear 