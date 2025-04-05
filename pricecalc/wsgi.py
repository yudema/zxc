"""
WSGI config for pricecalc project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and other commands will use this.
"""

import os
import sys

# Добавляем директории проекта в sys.path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_PATH)

# Добавляем директорию pricecalc/ в sys.path
PRICECALC_APP_PATH = os.path.join(BASE_PATH, 'pricecalc')
if PRICECALC_APP_PATH not in sys.path:
    sys.path.insert(0, PRICECALC_APP_PATH)

# Перенаправляем на правильный wsgi-модуль в pricecalc/pricecalc/
from pricecalc.wsgi import application 