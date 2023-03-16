import configparser
from pathlib import Path
from typing import Any, Iterable, List, Optional, Union

from ignf_gpf_api.pattern.Singleton import Singleton
from ignf_gpf_api.io.OutputManager import OutputManager
from ignf_gpf_api.io.Errors import ConfigReaderError


class Config(metaclass=Singleton):
    """Classe singleton de gestion de la configuration.

    Attributes:
        __config_parser (configparser): ConfigParser
        __ini_file_path (string): Chemin vers le fichier de configuration BaGI
    """

    conf_dir_path = Path(__file__).parent.parent.absolute() / "_conf"
    data_dir_path = Path(__file__).parent.parent.absolute() / "_data"
    ini_file_path = conf_dir_path / "default.ini"

    def __init__(self) -> None:
        """A l'instanciation, le fichier par défaut est lu.

        Il faudra ensuite surcharger les paramètres en lisant d'autres fichiers via la méthode `read`.

        Raises:
            ConfigReaderError: levée si le fichier de configuration par défaut n'est pas trouvé
        """
        self.__output_manager: OutputManager = OutputManager()

        if not Config.ini_file_path.exists():
            raise ConfigReaderError("Fichier de configuration par défaut {ConfigReader.ini_file_path} non trouvé.")

        self.__config_parser: configparser.ConfigParser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        with Config.ini_file_path.open(encoding="UTF-8") as f_ini:
            self.__config_parser.read_file(f_ini)

        # Définition du niveau de log pour l'OutputManager par défaut
        self.__output_manager.set_log_level(self.get("logging", "log_level"))

    def set_output_manager(self, output_manager: Any) -> None:
        self.__output_manager = output_manager

    @property
    def om(self) -> OutputManager:
        return self.__output_manager

    def read(self, filenames: Union[str, Path, Iterable[Union[str, Path]]]) -> List[str]:
        """Permet de surcharger la configuration en lisant un ou plusieurs nouveau(x) fichier(s) de configuration.

        Les derniers fichiers ont la priorité. Si un fichier n'est pas trouvé, aucune erreur n'est levée.
        La fonction retourne la liste des fichiers lus.

        Args:
            filenames (Union[str, Path, Iterable[Union[str, Path]]]): Chemin ou liste des chemins vers le ou les fichier(s) à lire

        Returns:
            liste des fichiers trouvés et lus
        """
        return self.__config_parser.read(filenames)

    def get_parser(self) -> configparser.ConfigParser:
        """Retourne le config_parser.

        Returns:
            le config parser
        """
        return self.__config_parser

    def get(self, section: str, option: str, fallback: Optional[str] = None) -> str:
        """Récupère la valeur associée au paramètre demandé.

        Args:
            section (str): section du paramètre
            option (str): option du paramètre
            fallback (Optional[str], optional): valeur par défaut.

        Returns:
            la valeur du paramètre
        """
        return self.__config_parser.get(section, option, fallback=fallback)  # type: ignore

    def get_int(self, section: str, option: str, fallback: Optional[int] = None) -> int:
        """Récupère la valeur associée au paramètre demandé, convertie en `int`.

        Args:
            section (str): section du paramètre
            option (str): option du paramètre
            fallback (Optional[int], optional): valeur par défaut.

        Returns:
            la valeur du paramètre
        """
        return self.__config_parser.getint(section, option, fallback=fallback)  # type: ignore

    def get_float(self, section: str, option: str, fallback: Optional[float] = None) -> float:
        """Récupère la valeur associée au paramètre demandé, convertie en `float`.

        Args:
            section (str): section du paramètre
            option (str): option du paramètre
            fallback (Optional[float], optional): valeur par défaut.

        Returns:
            la valeur du paramètre
        """
        return self.__config_parser.getfloat(section, option, fallback=fallback)  # type: ignore

    def get_bool(self, section: str, option: str, fallback: Optional[bool] = None) -> bool:
        """Récupère la valeur associée au paramètre demandé, convertie en `bool`.

        Args:
            section (str): section du paramètre
            option (str): option du paramètre
            fallback (Optional[bool], optional): valeur par défaut.

        Returns:
            la valeur du paramètre
        """
        return self.__config_parser.getboolean(section, option, fallback=fallback)  # type: ignore

    def get_temp(self) -> Path:
        """Récupère le chemin racine du dossier temporaire à utiliser.

        Returns:
            chemin racine du dossier temporaire à utiliser
        """
        return Path(self.get("miscellaneous", "tmp_workdir"))
