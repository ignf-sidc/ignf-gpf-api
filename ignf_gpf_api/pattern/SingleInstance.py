from typing import Any, Dict, Union


class SingleInstance(type):
    """Define an Instance operation that lets clients access its unique
    instance with this args

    exemple :
        class MyClass(metaclass=SingleInstance):
            def __init__(self, a, b):
                pass
        MyClass('a', 0) == MyClass('a', 0)
        MyClass('a', 0) != MyClass('a', 1)
    """

    _instance: Dict[Union[int, str], Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Fonction pour vérifier s'il faut instancier ou pas le singleton.

        Returns:
            object: objet instancié
        """
        id_ = args[0]
        if id_ not in cls._instance:
            cls._instance[id_] = super().__call__(*args, **kwargs)
        return cls._instance[id_]
