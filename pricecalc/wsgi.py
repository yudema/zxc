"""
WSGI config for pricecalc project.
"""

import os
import sys

# Добавляем текущую директорию в PYTHONPATH
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricecalc.settings')

application = get_wsgi_application() 