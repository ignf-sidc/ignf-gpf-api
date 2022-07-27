from typing import Any, Dict
from ignf_gpf_api.workflow.resolver.AbstractResolver import AbstractResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolveDataUsernameNotFound


class UserResolver(AbstractResolver):
    """Classe permettant de récupérer les informations sur l'utilisateur authentifié.

    Attributes :
        __name (str): nom de code du resolver
        __username_data (Dict[str, Any]): liste des infos de l'utilisateur authentifié
    """

    def __init__(self, name: str, username_data: Dict[str, Any]) -> None:
        """Constructeur.

                Args:
                    name (str): nom du résolveur
                    username_data (Dict[str, Any]): liste de clé/valeur à
        utiliser
        """
        super().__init__(name)
        self.__username_data: Dict[str, Any] = username_data

    def resolve(self, string_to_solve: str) -> Any:
        """résoudre la chaîne de caractères pour récupérer les infos de l'utilisateur

        Args:
            string_to_solve (str): chaîne de caractères à résoudre

        Raises:
            ResolveDataUsernameNotFound: gérer l'erreur quand l'info de l'utilisateur n'est pas récupérée

        Returns:
            str: chaîne de caractères résolue
        """
        # La chaîne à résoudre est en fait la clé, donc il suffit de renvoyer la valeur associée
        if string_to_solve in self.__username_data:
            return str(self.__username_data[string_to_solve])
        # Sinon on lève une exception
        raise ResolveDataUsernameNotFound(self.name, string_to_solve)
