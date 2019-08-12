from django.apps import AppConfig


class AppAuthConfig(AppConfig):
    name = 'app_auth'

    def ready(self):
        import app_auth.signals
