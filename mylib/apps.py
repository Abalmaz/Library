from django.apps import AppConfig


class MylibConfig(AppConfig):
    name = 'mylib'

    def ready(self):
        import mylib.signals