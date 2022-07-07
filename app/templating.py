from datetime import datetime

from jinja2 import Environment, PackageLoader
from roconfiguration import Configuration

from blacksheep.server import Application
from blacksheep.server.templating import use_templates


def configurare_templating(
    application: Application, configuration: Configuration
) -> None:
    """Configureaza sabloanele HTML la nivel de server web folosind Jinja2."""
    use_templates(application, PackageLoader("app", "views"))

    def get_copy():
        now = datetime.now()
        return "{} {}".format(now.year, configuration.site.copyright)

    helpers = {"_": lambda x: x, "copy": get_copy}

    env: Environment = application.jinja_environment
    env.globals.update(helpers)
