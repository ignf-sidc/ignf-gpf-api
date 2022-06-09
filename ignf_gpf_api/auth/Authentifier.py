import time
import traceback
from http import HTTPStatus
from typing import Dict, Optional
import requests

from ignf_gpf_api.pattern.Singleton import Singleton
from ignf_gpf_api.auth.Token import Token
from ignf_gpf_api.auth.Errors import AuthentificationError
from ignf_gpf_api.io.Config import Config


class Authentifier(metaclass=Singleton):
    """Singleton permettant de s'authentifier auprès du serveur KeyCloak.

    Attributes :
        __token_url (str) : url permettant de récupérer le jeton d'authentification
        __login (str) : login pour l'authentification
        __password (str) : password pour l'authentification
        __client_id (str) : identification client devant être donné au serveur d'authentification
        __nb_attempts  (int) : nombre de tentatives possibles en cas de problème rencontré pendant la récupération du jeton
        __sec_between_attempt (int) : nombre de secondes entre deux tentatives en cas de problème rencontré pendant la récupération du jeton
        __last_token (Token) : sauvegarde du dernier jeton récupéré (pour éviter de multiples requêtes au serveur KeyCloak)
    """

    def __init__(self) -> None:
        """Constructeur."""
        # Sauvegarde de la conf comme attributs d'instance
        self.__token_url: str = Config().get("store_authentification", "token_url")
        self.__login: str = Config().get("store_authentification", "login")
        self.__password: str = Config().get("store_authentification", "password")
        self.__client_id: str = Config().get("store_authentification", "client_id")
        self.__nb_attempts: int = Config().get_int("store_authentification", "nb_attempts")
        self.__sec_between_attempt: int = Config().get_int("store_authentification", "sec_between_attempt")
        # Permettra la sauvegarde du dernier jeton récupéré (pour éviter de multiples requêtes au serveur KeyCloak)
        self.__last_token: Optional[Token] = None

    def __request_new_token(self, nb_attempts: int) -> None:
        """Récupère un nouveau jeton de zéro et le sauvegarde
        En cas de problème pendant la récupération, essaie nb_attempts fois en attendant __sec_between_attempt secondes entre plusieurs tentatives
        Args:
            nb_attempts (int): nombre de tentatives restantes en cas d'erreur
        Raises :
            Exception : liée à la requête http, levée si la récupération de jeton au bout de nb_attempts tentatives
        """
        o_response = None
        try:
            # Requête KeyCloak de récupération du jeton
            o_response = requests.post(
                self.__token_url,
                data={
                    "grant_type": "password",
                    "username": self.__login,
                    "password": self.__password,
                    "client_id": self.__client_id,
                },
                headers={
                    "content-type": "application/x-www-form-urlencoded",
                },
            )
            if o_response.status_code == HTTPStatus.OK:
                self.__last_token = Token(o_response.json())
            else:
                raise requests.exceptions.HTTPError(f"Code retour authentification KeyCloak = {o_response.status_code}")

        except Exception as e_error:
            Config().om.warning("La récupération du jeton d'authentification a échoué...")
            # Affiche la pile d'exécution
            Config().om.debug(traceback.format_exc())
            # Une erreur s'est produite : attend un peu et relance une nouvelle fois la fonction
            if nb_attempts > 0:
                time.sleep(self.__sec_between_attempt)
                self.__request_new_token(nb_attempts - 1)
            # Le nombre de tentatives est atteint : comme dirait Jim, this is the end...
            else:
                Config().om.error(f"La récupération du jeton d'authentification a échoué après {self.__nb_attempts} tentatives")
                raise e_error

    def get_access_token_string(self) -> str:
        """Retourne le jeton d'authentification sous forme de chaîne de caractères
        Returns:
            str : un jeton valide
        Raises :
            AuthentificationError : si la récupération de jeton au bout de nb_attempts tentatives
        """
        try:
            while (self.__last_token is None) or (self.__last_token.is_valid() is False):
                self.__request_new_token(self.__nb_attempts)
            return self.__last_token.get_access_string()
        except Exception as e_error:
            s_error_message = f"La récupération du jeton d'authentification a échoué après {self.__nb_attempts} tentatives"
            Config().om.error(s_error_message)
            raise AuthentificationError(s_error_message) from e_error

    def get_http_header(self, json_content_type: bool = False) -> Dict[str, str]:
        """Renvoie une entête http d'authentification à destination de KeyCloak et consommable par une requête via le module requests
        Args :
            json_content_type (bool) : indique si le content type json doit être spécifié (par défaut False)
        Returns :
            Dict[str, str] : dictionnaire de la forme {"Authorization": "Bearer <JETON>", "content-type":"application/json"}
        Raises :
            AuthentificationError : si la récupération de jeton a posé problème
        """
        d_http_header = {"Authorization": f"Bearer {self.get_access_token_string()}"}
        if json_content_type:
            d_http_header["content-type"] = "application/json"
        return d_http_header

    def revoke_token(self) -> None:
        """Révoque le token actuellement utilisé pour forcer la récupération d'un nouveau token."""
        self.__last_token = None
