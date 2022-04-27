from ignf_gpf_api.Error import GpfApiError


class ConfigReaderError(GpfApiError):
    """Est levée quand il y a un problème pendant la lecture du fichier de configuration.

    Attributes:
        __message (str): message décrivant le problème
    """
