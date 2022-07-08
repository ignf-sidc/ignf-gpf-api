from abc import ABC, abstractmethod


class AbstractResolver(ABC):
    """Classe abstraite permettant de résoudre le paramétrage des fichiers d'action.

    Attributes :
        __name (str): nom de code du resolver
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self.__name: str = name

    @abstractmethod
    def resolve(self, string_to_solve: str) -> str:
        """Résout la chaîne à traiter et retourne la chaîne obtenue.

        Args:
            string_to_solve (str): chaîne à résoudre

        Returns:
            str: chaîne résolue
        """

    @property
    def name(self) -> str:
        return self.__name
