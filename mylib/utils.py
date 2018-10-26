from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.core.cache import cache


def show_toolbar(request):
    if request.is_ajax():
        return False
    return True


def invalidate_cache(path=''):
    request = HttpRequest()
    request.META = {'SERVER_NAME': 'localhost', 'SERVER_PORT': 8000}
    request.LANGUAGE_CODE = 'en-us'
    request.path = path

    try:
        cache_key = get_cache_key(request)
        if cache_key:
            if cache.has_key(cache_key):
                cache.delete(cache_key)
                return (True, 'successfully invalidated')
            else:
                return (False, 'cache_key does not exist in cache')
        else:
            raise ValueError('failed to create cache_key')
    except (ValueError, Exception) as e:
        return (False, e)
