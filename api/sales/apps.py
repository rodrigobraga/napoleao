from django.apps import AppConfig
from django.db.models.signals import post_save


class SalesConfig(AppConfig):
    name = 'sales'
    
    def ready(self):
        from .models import Sale
        from .receivers import approve_on_create

        post_save.connect(approve_on_create, sender=Sale)
