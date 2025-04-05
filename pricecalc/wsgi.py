"""
WSGI config for pricecalc project.
"""

import os
import sys

# Настраиваем пути Python из специального модуля
try:
    from setup_python_path import setup_python_paths
    setup_python_paths()
except ImportError:
    # Если модуль не найден, настраиваем пути вручную
    current_path = os.path.dirname(os.path.abspath(__file__))
    if current_path not in sys.path:
        sys.path.insert(0, current_path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricecalc.settings')

application = get_wsgi_application() 