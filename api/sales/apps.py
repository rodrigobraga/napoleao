from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class SalesConfig(AppConfig):
    name = 'sales'
    
    def ready(self):
        from .models import Sale
        from .receivers import (
            approve_on_create,
            process_on_change_handler,
            process_on_delete_handler
        )

        post_save.connect(approve_on_create, sender=Sale)
        post_save.connect(process_on_change_handler, sender=Sale)

        post_delete.connect(process_on_delete_handler, sender=Sale)
