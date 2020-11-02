from django.apps import AppConfig


class FinderConfig(AppConfig):
    name = 'finder'

    def ready(self):
        import finder.signals