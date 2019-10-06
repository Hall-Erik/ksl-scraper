from django.apps import AppConfig


class JobsAuthConfig(AppConfig):
    name = 'jobs_auth'

    def ready(self):
        import jobs_auth.signals  # noqa: F401
