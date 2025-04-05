from django.core.cache import cache
from django.http import HttpResponseTooManyRequests
import time

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_prefix = 'ratelimit'
        self.limit = 100  # Максимальное количество запросов
        self.window = 60  # Временное окно в секундах

    def __call__(self, request):
        if not self._should_limit(request):
            return self.get_response(request)

        ip = self._get_client_ip(request)
        key = f"{self.cache_prefix}_{ip}"
        
        # Получаем текущее время и список временных меток запросов
        now = time.time()
        requests = cache.get(key, [])
        
        # Удаляем старые запросы
        requests = [req for req in requests if now - req < self.window]
        
        if len(requests) >= self.limit:
            return HttpResponseTooManyRequests("Too many requests. Please try again later.")
        
        # Добавляем текущий запрос
        requests.append(now)
        cache.set(key, requests, self.window)
        
        return self.get_response(request)

    def _should_limit(self, request):
        """Определяет, нужно ли ограничивать запрос"""
        # Не ограничиваем статические файлы и админку
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return False
        
        # Не ограничиваем GET запросы к главной странице
        if request.method == 'GET' and request.path == '/':
            return False
            
        return True

    def _get_client_ip(self, request):
        """Получает IP-адрес клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR') 