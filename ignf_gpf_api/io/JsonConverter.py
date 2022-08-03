from __future__ import unicode_literals

import datetime
import json as JSON
from typing import Any, Dict, Optional

from ignf_gpf_api.pattern.Singleton import Singleton
from ignf_gpf_api.io.Config import Config


class JsonConverter(metaclass=Singleton):
    """Classe de conversion des objects python en json. Le but est de convertir
    les objets qui ne sont pas nativement gérés par Python comme les dates."""

    def __init__(self) -> None:
        """initialisation : liste des routes et adresse site"""
        # Stockage en attributs de classe des patterns
        self.__datetime_pattern = Config().get("json_converter", "datetime_pattern")
        self.__date_pattern = Config().get("json_converter", "date_pattern")
        self.__time_pattern = Config().get("json_converter", "time_pattern")

    def dumps(self, data: Dict[Any, Any]) -> str:
        """Cette fonction permet de convertir les classes python en string JSON.
        Pour le moment, sont traitées les dates, times, et datetimes.
        On utilise un "converter" spécialisé.

        Args:
            data (Any): données à envoyer à l'api avec des classes python

        Returns:
            str: JSON avec gestion des classes Python
        """
        if data is None:
            return None
        s_json = JSON.dumps(data, default=self.__converter)
        return s_json

    def convert(self, data: Any) -> Any:
        """Passe en string les objets non gérés nativement en JSON par Python.
        Ex : {"date": date(2020, 1, 1)} => {"date": "2020-01-01"}

        Args:
            data (Any): données à envoyer à l'api avec des classes python

        Returns:
            Any: données à envoyer à l'api sans classe python
        """
        if data is None:
            return None
        s_json = self.dumps(data)
        return JSON.loads(s_json)

    def __converter(self, obj: object) -> Optional[str]:
        """Converter spécialisé pour passer des classes python au json.

        Args:
            obj (object): objet à convertir

        Returns:
            str: objet converti
        """
        if isinstance(obj, datetime.datetime):
            return obj.strftime(self.__datetime_pattern)
        if isinstance(obj, datetime.date):
            return obj.strftime(self.__date_pattern)
        if isinstance(obj, datetime.time):
            return obj.strftime(self.__time_pattern)
        return None


if __name__ == "__main__":
    o_json_converter = JsonConverter()
    python_data = {
        "date": datetime.date.today(),
        "time": datetime.datetime.now().time(),
        "datetime": datetime.datetime.now(),
    }
    text_data = o_json_converter.convert(python_data)
    print(JSON.dumps(text_data, indent=4))
