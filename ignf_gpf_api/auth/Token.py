from datetime import datetime
from datetime import timedelta
from typing import Any, Dict


class Token:
    """Représente un jeton KeyCloak. Ce jeton est caractérisé par ensemble d'informations clé-valeur et une date d'expiration.

    Attributes:
        __token_dict (dict): Stockage du jeton `{"access_token": "valeur-du-jeton", "expires_in": temps-en-secondes}`
        __expiration_date (datetime): Date d'expiration du jeton
    """

    def __init__(self, token_dict: Dict[str, Any]) -> None:
        """À l'instanciation : on stocke l'ensemble d'informations clé-valeur et on calcule la date d'expiration à partir de son délai d'expiration.

        Args:
            token_dict (dict): Jeton tel que renvoyé par le service d'authentification : `{"access_token": "valeur-du-jeton", "expires_in": temps-en-secondes}`
        """
        self.__token_dict: Dict[str, Any] = token_dict
        self.__expiration_date: datetime = datetime.now() + timedelta(seconds=token_dict["expires_in"])

    def is_valid(self) -> bool:
        """Indique si le jeton est valide par rapport à sa date d'expiration.

        Returns:
            bool: `True` si le jeton est valide
        """
        return datetime.now() < self.__expiration_date

    def get_access_string(self) -> str:
        """Retourne le jeton d'authentification sous forme de chaîne de caractères.

        Returns:
            str: Jeton d'accès
        """
        return str(self.__token_dict["access_token"])
