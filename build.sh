#!/usr/bin/env bash
# exit on error
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Миграции базы данных
cd pricecalc
python manage.py migrate

# Соберем статику, если необходимо
python manage.py collectstatic --no-input 