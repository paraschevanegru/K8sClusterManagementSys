"""
Folosim acest modul pentru a inregistra serviciile necesare
"""
from typing import Tuple
from roconfiguration import Configuration
from rodi import Container
from core.events import ServicesRegistrationContext


def configurare_services(
    configuration: Configuration,
) -> Tuple[Container, ServicesRegistrationContext, Configuration]:
    """Configurarea serviciilor"""
    container = Container()

    context = ServicesRegistrationContext()

    container.add_instance(configuration)

    return container, context, configuration
