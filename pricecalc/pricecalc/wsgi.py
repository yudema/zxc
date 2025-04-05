"""
WSGI config for pricecalc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Добавляем текущий каталог и родительский каталог в путь Python
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.dirname(base_dir)

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricecalc.pricecalc.settings')

application = get_wsgi_application()
