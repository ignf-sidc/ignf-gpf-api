from ignf_gpf_api.Errors import GpfApiError


class AuthentificationError(GpfApiError):
    """Est levée quand un problème apparaît durant la récupération d'informations d'authentification

    Attr:
        __message (str): message décrivant le problème
    """
