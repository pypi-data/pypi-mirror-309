# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Configuration
from django.core.cache import cache
from django_variable.utils import set_cache_configuration

@receiver(post_save, sender=Configuration)
def set_cache(sender, instance, created, **kwargs):
    set_cache_configuration()
