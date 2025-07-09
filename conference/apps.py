from django.apps import AppConfig


class ConferenceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "conference"

class conference(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conference'

    def ready(self):
        import conference.signals
