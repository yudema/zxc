"""
Настройка путей Python для проекта
"""

import os
import sys

def setup_python_paths():
    """Настраивает пути Python для проекта."""
    # Получаем путь к текущей директории (pricecalc)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Добавляем текущую директорию в sys.path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Добавляем родительскую директорию в sys.path
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

# Автоматически выполняем при импорте
setup_python_paths() 