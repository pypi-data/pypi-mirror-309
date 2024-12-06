from .models import Configuration
from django.core.cache import cache

def get_config(key, default=None):
    try:
        value = cache.get(key)
        if value is None:
            value = Configuration.objects.get(key=key).value
            cache.set(key, value)
        return value

    except Configuration.DoesNotExist:
        if default is not None:
            set_config(key, default)

        return default

def set_config(key, value):
    config, created = Configuration.objects.get_or_create(key=key)
    config.value = value
    config.save()
    cache.set(key, value)


def set_cache_configuration():
    configurations = Configuration.objects.all()
    for configuration in configurations:
        cache.set(configuration.key, configuration.value)