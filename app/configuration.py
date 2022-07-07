from roconfiguration import Configuration


def incarcare_configuratie() -> Configuration:
    configuration = Configuration()

    # Incarcare setari dintr-un fisier yaml
    configuration.add_yaml_file("settings.yaml")
    configuration.add_environmental_variables()

    return configuration
