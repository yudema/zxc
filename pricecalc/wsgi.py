"""
WSGI config for pricecalc project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

# Добавляем директории проекта в sys.path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_PATH)

# Настраиваем переменные окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricecalc.settings')

# Создаем WSGI приложение
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 