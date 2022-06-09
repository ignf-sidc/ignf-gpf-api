class GpfApiError(Exception):
    """Erreur générique levée pour signaler un problème en présentant un mesage à destination e l'utilisateur final.

    Attributes:
        __message (str): message décrivant le problème
    """

    def __init__(self, message: str) -> None:
        """Constructor

        Args:
            message (str) : message décrivant le problème
        """
        super().__init__()
        self.__message: str = message

    def __str__(self) -> str:
        return self.__message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__message})"

    @property
    def message(self) -> str:
        return self.__message
