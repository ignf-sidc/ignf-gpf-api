import json
from typing import Any, Dict, Optional, List, Union

from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.io.Color import Color


class ConfigReaderError(GpfApiError):
    """Erreur levée quand il y a un problème pendant la lecture du fichier de configuration par défaut.

    Attributes:
        __message (str): message décrivant le problème
    """


class RoutingReaderError(GpfApiError):
    """Erreur levée quand il y a un problème pendant la lecture du fichier de configuration des routes.

    Attributes:
        __message (str): message décrivant le problème
    """


class ApiError(Exception):
    """Erreur API : classe abstraite pour gérer les erreurs API en général."""


class RouteNotFoundError(ApiError):
    """Route non trouvée (problème de configuration)."""

    def __init__(self, route_name: str) -> None:
        """Instanciée à partir du nom de la route non trouvée.

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
    """Erreur API : erreur générique et sans réponse lors d'une requête à l'API."""

    def __init__(self, url: str, method: str, params: Optional[Dict[str, Any]], data: Optional[Union[Dict[str, Any], List[Any]]]) -> None:
        """Instanciée à partir de l'URL, la méthode, les paramètres et les données posant problème.

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
                "Erreur au requêtage de la Géoplateforme.",
                f"Explication : {self.__doc__}",
                "Détails : ",
                f"   * url: {self.url}",
                f"   * method: {self.method}",
                f"   * params: {self.params}",
                f"   * data: {self.data}",
            ]
        )


class InternalServerError(AbstractRequestError):
    """Erreur API : erreur interne à l'API (contactez le support)."""


class NotFoundError(AbstractRequestError):
    """Erreur API : entité non trouvée sur la Géoplateforme."""


class NotAuthorizedError(AbstractRequestError):
    """Erreur API : action non autorisée."""

    def __init__(self, url: str, method: str, params: Optional[Dict[str, Any]], data: Optional[Union[Dict[str, Any], List[Any]]], response: str):
        """Instanciée à partir de l'URL, la méthode, les paramètres et les données posant problème ainsi que la réponse de l'API.

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
                f"   * response: {self.response}",
            ]
        )


class _WithResponseError(AbstractRequestError):
    """Erreur API : erreur générique avec réponse lors d'une requête à l'API."""

    def __init__(self, url: str, method: str, params: Optional[Dict[str, Any]], data: Optional[Union[Dict[str, Any], List[Any]]], response: str):
        """Instanciée à partir de l'URL, la méthode, les paramètres et les données posant problème ainsi que la réponse de l'API.

        Args:
            url (str): url de la requête
            method (str): méthode de la requête
            params (Optional[Dict[str, Any]]): paramètres de la requête
            data (Optional[Union[Dict[str, Any], List[Any]]]): données envoyées
            response (str): données reçues
        """
        super().__init__(url, method, params, data)
        self.response_str = response
        self.response_data = None
        # On tente de parser la réponse
        try:
            self.response_data = json.loads(self.response_str)
        except json.JSONDecodeError:
            # Le parsing a échoué, pas grave
            pass

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        # Affichage de base
        l_str = [
            f"{super().__repr__()}",
            f"   * response: {self.response_str}",
        ]
        # Affichage si response_data
        if self.response_data is not None:
            # On tente de récupérer "error"
            if "error" in self.response_data:
                l_str.append(f"   * error: {Color.BOLD}{self.response_data['error']}{Color.END}")
            # On tente de récupérer "error_description"
            if "error_description" in self.response_data:
                l_str.append(f"   * error_description: {Color.BOLD}{self.response_data['error_description']}{Color.END}")
        return "\n".join(l_str)


class BadRequestError(_WithResponseError):
    """Erreur API : mauvaise requête (contactez le support)."""


class ConflictError(_WithResponseError):
    """Erreur API : conflit au traitement de la requête (Est-ce que vous tentez de supprimer une ressource utilisée ?)."""


class StatusCodeError(_WithResponseError):
    """Erreur API : erreur avec un code de retour non prévu par une erreur explicite..."""

    def __init__(
        self,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]],
        data: Optional[Union[Dict[str, Any], List[Any]]],
        status_code: int,
        response: str,
    ):
        """Instanciée à partir de l'URL, la méthode, les paramètres et les données posant problème ainsi que la réponse et le code de retour de l'API.

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
                f"   * status_code: {self.status_code}",
            ]
        )
