from typing import Any, Dict

from ignf_gpf_api.workflow.resolver.AbstractResolver import AbstractResolver
from ignf_gpf_api.workflow.resolver.Errors import ResolverError


class DictResolver(AbstractResolver):
    """Classe permettant de résoudre des paramètres clé -> valeur.

    Attributes :
        __name (str): nom de code du resolver
        __key_value (Dict[str, Any]): liste des paramètres à résoudre
    """

    def __init__(self, name: str, key_value: Dict[str, Any]) -> None:
        """Constructeur.

        Args:
            name (str): nom du résolveur
            key_value (Dict[str, Any]): liste de clé/valeur à utiliser
        """
        super().__init__(name)
        self.__key_value: Dict[str, Any] = key_value

    def resolve(self, string_to_solve: str) -> str:
        # La chaîne à résoudre est en fait la clé, donc il suffit de renvoyer la valeur associée
        if string_to_solve in self.__key_value:
            return str(self.__key_value[string_to_solve])
        # Sinon on lève une exception
        raise ResolverError(self.name, string_to_solve)
