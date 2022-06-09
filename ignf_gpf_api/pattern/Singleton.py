from typing import Any, Optional


class Singleton(type):
    """Define an Instance operation that lets clients access its unique
    instance of class.

    exemple :
        class MyClass(metaclass=Singleton):
            def __init__(self):
                pass
    """

    _instance: Optional[Any] = None

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Fonction pour vérifier s'il faut instancier ou pas le singleton.

        Returns:
            object: objet instancié
        """
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
