from roconfiguration import Configuration
from rodi import Container

from blacksheep.server import Application
from core.events import ServicesRegistrationContext

from . import controllers
from .errors import configurare_error_handlers
from .templating import configurare_templating


async def before_start(application: Application) -> None:
    application.services.add_instance(application)
    application.services.add_alias("app", Application)


def configurare_aplicatie(
    services: Container,
    context: ServicesRegistrationContext,
    configuration: Configuration,
) -> Application:
    app = Application(
        services=services,
        show_error_details=configuration.show_error_details,
        debug=configuration.debug,
    )
    """Configurare aplicatie."""

    app.on_start += before_start

    app.on_start += context.initialize
    app.on_stop += context.dispose

    configurare_error_handlers(app)
    configurare_templating(app, configuration)

    app.serve_files("app/static")

    return app
