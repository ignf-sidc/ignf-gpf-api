import json
from typing import Any, Dict, Optional, List, Union
from ignf_gpf_api.Errors import GpfApiError


class ConfigReaderError(GpfApiError):
    """Est levée quand il y a un problème pendant la lecture du fichier de configuration.

    Attributes:
        __message (str): message décrivant le problème
    """


class RoutingReaderError(GpfApiError):
    """Est levée quand il y a un problème pendant la lecture du fichier de configuration des routes.

    Attributes:
        __message (str): message décrivant le problème
    """


class ApiError(Exception):
    """Erreur API : classe abstraite"""


class RouteNotFoundError(ApiError):
    """Route non trouvée (problème de configuration)."""

    def __init__(self, route_name: str) -> None:
        """Constructeur.

        Args:
            route_name (str): nom de la route manquante
        """
        super().__init__()
        self.route_name = route_name

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "\n".join(
            [
                f"Explications : {self.__doc__}\n",
                f"La route demandée '{self.route_name}' n'existe pas dans la configuration.",
            ]
        )


class AbstractRequestError(ApiError):
    """Erreur générique de requête à l'API"""

    def __init__(self, url: str, method: str, params: Optional[Dict[str, Any]], data: Optional[Union[Dict[str, Any], List[Any]]]) -> None:
        """Constructeur.

        Args:
            url (str): url de la requête
            method (str): méthode de la requête
            params (Optional[Dict[str, Any]]): paramètres de la requête
            data (Optional[Union[Dict[str, Any], List[Any]]]): données envoyées
        """
        super().__init__()
        self.url = url
        self.method = method
        self.params = params
        self.data = json.dumps(data)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "\n".join(
            [
                f"Explications : {self.__doc__}",
                f"url: {self.url}",
                f"method: {self.method}",
                f"params: {self.params}",
                f"data: {self.data}",
            ]
        )


class InternalServerError(AbstractRequestError):
    """Erreur interne à l'API (contactez le support)."""


class NotFoundError(AbstractRequestError):
    """Entité non trouvée."""


class NotAuthorizedError(AbstractRequestError):
    """Action non autorisée"""

    def __init__(self, url: str, method: str, params: Optional[Dict[str, Any]], data: Optional[Union[Dict[str, Any], List[Any]]], response: str):
        """Constructeur.

        Args:
            url (str): url de la requête
            method (str): méthode de la requête
            params (Optional[Dict[str, Any]]): paramètres de la requête
            data (Optional[Union[Dict[str, Any], List[Any]]]): données envoyées
            response (str): données reçues
        """
        super().__init__(url, method, params, data)
        self.response = response

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "\n".join(
            [
                f"{super().__repr__()}",
                f"response: {self.response}",
            ]
        )


class _WithResponseError(AbstractRequestError):
    """Erreur avec réponse."""

    def __init__(self, url: str, method: str, params: Optional[Dict[str, Any]], data: Optional[Union[Dict[str, Any], List[Any]]], response: str):
        """Constructeur.

        Args:
            url (str): url de la requête
            method (str): méthode de la requête
            params (Optional[Dict[str, Any]]): paramètres de la requête
            data (Optional[Union[Dict[str, Any], List[Any]]]): données envoyées
            response (str): données reçues
        """
        super().__init__(url, method, params, data)
        self.response_dumps = json.dumps(response)
        self.response = response

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "\n".join(
            [
                f"{super().__repr__()}",
                f"response: {self.response_dumps}",
            ]
        )


class BadRequestError(_WithResponseError):
    """Mauvaise requête"""


class StatusCodeError(_WithResponseError):
    """Erreur avec un "status code" non prévu par une erreur explicite..."""

    def __init__(
        self,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]],
        data: Optional[Union[Dict[str, Any], List[Any]]],
        status_code: int,
        response: str,
    ):
        """Constructeur.

        Args:
            url (str): url de la requête
            method (str): méthode de la requête
            params (Optional[Dict[str, Any]]): paramètres de la requête
            data (Optional[Union[Dict[str, Any], List[Any]]]): données envoyées
            status_code (int): code de retour
            response (str): données reçues
        """
        super().__init__(url, method, params, data, response)
        self.status_code = status_code

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "\n".join(
            [
                f"{super().__repr__()}",
                f"status_code: {self.status_code}",
            ]
        )
