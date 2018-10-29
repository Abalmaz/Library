from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.core.cache import cache


def show_toolbar(request):
    if request.is_ajax():
        return False
    return True


def invalidate_cache(book_path):
    host_name = get_current_site(None).name
    host_port = 8000
    request = HttpRequest()
    request.META = {'SERVER_NAME': host_name,
                    'SERVER_PORT': host_port}
    request.LANGUAGE_CODE = 'en-us'
    request.path = ''.join([host_name, book_path])

    try:
        cache_key = get_cache_key(request, key_prefix='book')
        if cache_key:
            if cache.has_key(cache_key):
                cache.delete(cache_key)
                return True, 'successfully invalidated'
            else:
                return False, 'cache_key does not exist in cache'
        else:
            raise ValueError('failed to create cache_key')
    except (ValueError, Exception) as e:
        return False, e
