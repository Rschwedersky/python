import os
from django import template
from django.core.cache import cache
from urllib.parse import unquote_plus, urlparse
from django.conf import settings

register = template.Library()


def get_database_info_by_url(url):
    def cast_urlstr(v):
        return unquote_plus(v) if isinstance(v, str) else v

    def cast_int(v):
        """Return int if possible."""
        return int(v) if hasattr(v, 'isdigit') and v.isdigit() else v

    parsed_url = urlparse(url)

    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed_url.path.lstrip('/'),
        'USER': cast_urlstr(parsed_url.username) or '',
        'PASSWORD': cast_urlstr(parsed_url.password) or '',
        'HOST': parsed_url.hostname or '',
        'PORT': cast_int(parsed_url.port) or '',
    }


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


def reset_cache(key, expiration_time=900):
    return cache.set(key, None, expiration_time)


def get_client_from_request(request):
    return request.user.profile.client


def get_django_channel_layer_backend():
    if settings.IS_LOCALHOST and settings.IS_DEV:
        return {
            "default": {
                "BACKEND": "channels.layers.InMemoryChannelLayer"
            }
        }
    else:
        return {
            "default": {
                "BACKEND": "channels_redis.core.RedisChannelLayer",
                "CONFIG": {
                    "hosts": [(os.environ.get('REDIS_HOST'), 6379)],
                },
            },
        }
