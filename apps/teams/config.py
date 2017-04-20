from django.apps import AppConfig
from django.db.models.signals import post_save


class TeamsAppConfig(AppConfig):
    name = 'teams'
    verbose_name = 'Participants'

    def ready(self):
        from .signals import result_saved
        post_save.connect(result_saved, dispatch_uid='result_saved')
