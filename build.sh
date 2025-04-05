#!/usr/bin/env bash
# exit on error
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Миграции базы данных
python pricecalc/manage.py migrate

# Соберем статику, если необходимо
python pricecalc/manage.py collectstatic --no-input 