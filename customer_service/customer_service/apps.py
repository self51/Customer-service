from django.apps import AppConfig
from django.conf import settings


class CustomerServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_service'

    def ready(self) -> None:
        """Initialize Dependency Injection after Django is fully loaded."""
        from customer_service.dependency_container import DependencyContainer

        container = DependencyContainer()
        container.config.from_dict(settings.__dict__)
        container.init_resources()
