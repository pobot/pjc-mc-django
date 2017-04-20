from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class EventAppConfig(AppConfig):
    name = 'event'
    verbose_name = "Gestion de l'événement"

    def ready(self):
        from .signals import result_changed
        for signal in (post_save, post_delete):
            signal.connect(result_changed, dispatch_uid='result_changed')
