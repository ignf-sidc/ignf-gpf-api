from datetime import datetime
from datetime import timedelta
from typing import Any, Dict


class Token:
    """Représente un jeton KeyCloak.
    Attributes :
        __token_dict (dict) : stockage du jeton {'access_token': 'valeur-du-jeton', 'expires_in': temps-en-secondes}
        __expiration_date (datetime) : date d'expiration du jeton
    """

    def __init__(self, token_dict: Dict[str, Any]) -> None:
        """Initialise le jeton avec une date d'expiration

        Args:
            token_dict (dict): {'access_token': 'valeur-du-jeton', 'expires_in': temps-en-secondes}
        """
        self.__token_dict: Dict[str, Any] = token_dict
        self.__expiration_date: datetime = datetime.now() + timedelta(seconds=token_dict["expires_in"])

    def is_valid(self) -> bool:
        """Indique si le jeton est valide

        Returns:
            bool: true si le jeton est valide
        """
        return datetime.now() < self.__expiration_date

    def get_access_string(self) -> str:
        """Retourne le jeton d'authentification sous forme de chaîne de caractères

        Returns:
            access_token (str): jeton d'accès
        """
        return str(self.__token_dict["access_token"])
