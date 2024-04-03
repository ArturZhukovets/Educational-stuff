# Django caching

# Caching a view
Для кэширования используя интерфейсы Django можно воспользоваться
1. Middleware
2. View cache decorator

Использование middleware не очень эффективно, так как потенциально
в оперативной памяти может одновременно храниться слишком много и статической и динамической информации.  
Рекомендуется использовать view cache decorator т.к он подходит для большинства кейсов.

```python
import datetime
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

BASE_URL = 'https://httpbin.org/'


@method_decorator(cache_page(60 * 5), name='dispatch')   # 60 * 5 - timeout 
class ApiCalls(TemplateView):
    template_name = 'apicalls/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get(f'{BASE_URL}/delay/2')
        response.raise_for_status()

        context['content'] = 'Results received!'
        context['current_time'] = datetime.datetime.now()
        return context
```

# Redis cache

1. Run redis with docker on port 6379 and RedisInsight on port 8001
```shell
docker run --rm -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```
2. pip install django-redis
3. add backend to settings.py
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```
В результате views обёрнутые декоратором cache будут полностью кэшироваться на уровне Expiration time.
При данном подходе кэшируется целиком весь отдаваемый Response, что будет выгодным не во всех кейсах.
Для более детального и точечного управления кэшированием можно рассмотреть `Low-Level Cache API`

# Memcached with Django
подробно описано здесь https://testdriven.io/blog/django-caching/ (как впрочем и всё view level кэширование)

***

# Low-Level Cache API in Django
link to article: https://testdriven.io/blog/django-low-level-cache/
