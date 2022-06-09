from __future__ import unicode_literals
from io import BufferedReader
import time
import traceback

from typing import Any, Dict, Optional, Tuple, List, Union
import requests

from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.auth.Authentifier import Authentifier
from ignf_gpf_api.pattern.Singleton import Singleton
from ignf_gpf_api.io.JsonConverter import JsonConverter
from ignf_gpf_api.io.Errors import ApiError, RouteNotFoundError, InternalServerError, NotFoundError, NotAuthorizedError, BadRequestError, StatusCodeError
from ignf_gpf_api.io.Config import Config


class ApiRequester(metaclass=Singleton):
    """Classe de requête à l'API GPF : gestion proxy, HTTPS et gestion des erreurs."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

    def __init__(self) -> None:
        # Récupération du convertisseur Json
        self.__jsonConverter = JsonConverter()
        self.__nb_attempts = Config().get_int("store_api", "nb_attempts")
        self.__sec_between_attempt = Config().get_int("store_api", "sec_between_attempt")

    def route_request(
        self,
        route_name: str,
        route_params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        files: Optional[Dict[str, Tuple[str, BufferedReader]]] = None,
    ) -> requests.Response:
        """Exécute une requête à l'API à partir du nom d'une route.

        Args:
            route_name (str): Route à utiliser
            route_params (Optional[Dict[str, Any]], optional): Paramètres obligatoires pour compléter la route. Defaults to None.
            params (Optional[Dict[str, Any]], optional): Paramètres optionnels de l'URL. Defaults to None.
            method (str, optional): méthode de la requête. Defaults to "GET".
            data (Optional[Dict[str, Any]], optional): Données de la requête. Defaults to None.
            files (Optional[Dict[str, Tuple[Any]]], optional): Liste des fichiers à envoyer {"file":('fichier.ext', File)}. Default to None.

        Raises:
            RouteNotFoundError: levée si la route demandée n'est pas définie dans les paramètres
            InternalServerError: levée si erreur interne de l'API
            NotFoundError: levée si l'entité demandée n'est pas trouvée par l'API
            NotAuthorizedError: levée si l'action effectuée demande d'autre autorisations
            BadRequestError: levée si la requête envoyée n'est pas correcte
            StatusCodeError: levée si un "status code" non prévu est récupéré

        Returns:
            requests.Response: réponse vérifiée
        """

        # La valeur par défaut est transformée en un dict valide
        if route_params is None:
            route_params = {}

        # On convertie les données Python en text puis en JSON
        data = self.__jsonConverter.convert(data)

        # On récupère la route
        s_route = Config().get("routing", route_name, fallback=None)
        if s_route is None:
            raise RouteNotFoundError(route_name)
        # On formate l'URL
        s_url = s_route.format(**route_params)

        # Exécution de la requête en boucle jusqu'au succès (ou erreur au bout d'un certains temps)
        return self.url_request(s_url, method, params, data, files)

    def url_request(
        self,
        url: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        files: Optional[Dict[str, Tuple[str, BufferedReader]]] = None,
    ) -> requests.Response:
        """Effectue une requête à l'API à partir d'une url. La retente plusieurs fois s'il y a un problème.

        Args:
            url (str): url absolue de la requête
            method (str, optional): méthode de la requête. Defaults to "GET".
            params (Optional[Dict[str, Any]], optional): paramètres. Defaults to None.
            data (Optional[Union[Dict[str, Any], List[Any]]], optional): données. Defaults to None.
            files (Optional[Dict[str, Tuple[Any]]], optional): fichiers. Defaults to None.

        Returns:
            requests.Response: réponse si succès
        """
        d_proxies = {
            "http": None,
            "https": None,
        }
        i_nb_attempts = 0
        while True:
            i_nb_attempts += 1
            try:
                # Définition du header
                d_headers = Authentifier().get_http_header(json_content_type=files is None)
                # Execution de la requête
                r = requests.request(url=url, params=params, json=data, method=method, headers=d_headers, proxies=d_proxies, files=files)  # type:ignore

                # Vérification du résultat...
                if r.status_code >= 200 and r.status_code < 300:
                    # Si c'est ok, on renvoie la réponse
                    return r
                if r.status_code == 500:
                    # Erreur interne (pas de retour)
                    raise InternalServerError(url, method, params, data)
                if r.status_code == 404:
                    # Element non trouvé (pas de retour)
                    raise NotFoundError(url, method, params, data)
                # Autre erreur (retour attendu)
                # on peut lever l'exception
                if r.status_code in (403, 401):
                    # Action non autorisée
                    Authentifier().revoke_token()  # On révoque le token
                    raise NotAuthorizedError(url, method, params, data, r.text)
                if r.status_code == 400:
                    # Requête incorrecte
                    raise BadRequestError(url, method, params, data, r.text)
                # Autre erreur
                raise StatusCodeError(url, method, params, data, r.status_code, r.text)

            except NotFoundError as e_error:
                # Si l'entité n'est pas trouvée, on ne retente pas, on sort directement en erreur
                s_message = f"L'élément demandé n'existe pas. Contactez le support si vous n'êtes pas à l'origine de la demande. URL : {e_error.url}."
                Config().om.error(s_message)
                raise GpfApiError(s_message) from e_error

            except (requests.HTTPError, requests.URLRequired) as e_error:
                # Affiche la pile d'exécution
                Config().om.debug(traceback.format_exc())
                # S'il y a une erreur d'URL, on ne retente pas, on indique de contacter le support
                s_message = "L'url indiquée en configuration est invalide ou inexistante. Contactez le support."
                Config().om.error(s_message)
                raise GpfApiError(s_message) from e_error

            except BadRequestError as e_error:
                # Affiche la pile d'exécution
                Config().om.debug(traceback.format_exc())
                # S'il y a une erreur de requête incorrecte, on ne retente pas, on indique de contacter le support
                s_message = "La requête formulée par le programme est incorrecte. Contactez le support."
                Config().om.error(s_message)
                raise GpfApiError(s_message) from e_error

            except (ApiError, requests.RequestException) as e_error:
                # Pour les autres erreurs, on retente selon les paramètres indiqués.
                # On récupère la classe de l'erreur histoire que ce soit plus parlant...
                s_title = e_error.__class__.__name__
                Config().om.warning(f"L'exécution d'une requête a échoué (tentative {i_nb_attempts}/{self.__nb_attempts})... ({s_title})")
                # Affiche la pile d'exécution
                Config().om.debug(traceback.format_exc())
                # Une erreur s'est produite : attend un peu et relance une nouvelle fois la fonction
                if i_nb_attempts < self.__nb_attempts:
                    time.sleep(self.__sec_between_attempt)
                # Le nombre de tentatives est atteint : comme dirait Jim, this is the end...
                else:
                    s_message = f"L'exécution d'une requête a échoué après {i_nb_attempts} tentatives"
                    Config().om.error(s_message)
                    raise GpfApiError(s_message) from e_error
