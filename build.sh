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

# Проверяем, есть ли приложение calculator в pricecalc
if [ ! -d "pricecalc/calculator" ]; then
  echo "Копирование приложения calculator в pricecalc..."
  if [ -d "calculator" ]; then
    cp -r calculator pricecalc/
  else
    echo "ОШИБКА: Приложение calculator не найдено!"
    exit 1
  fi
fi

# Миграции базы данных и статика
cd pricecalc
python manage.py migrate
python manage.py collectstatic --no-input --clear 