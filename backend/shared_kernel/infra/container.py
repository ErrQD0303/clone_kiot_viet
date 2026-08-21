"""Defines the application container for dependency injection."""
from dependency_injector import containers

class AppContainer(containers.DeclarativeContainer):  # pylint: disable=c-extension-no-member
    """Application container class for dependency injection."""
    wiring_config = containers.WiringConfiguration(  # pylint: disable=c-extension-no-member
        modules=[
        ]
    )
