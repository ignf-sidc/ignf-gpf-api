from pathlib import Path
from typing import Any, Dict, List


class Dataset:
    """Classe portante les infos nécessaires à la création d'une livraison et issues du dataset.

    Attributes :
        __data_dirs (List[Path]) : liste des dossiers à envoyer à l'API
        __upload_infos (Dict[str, str]) : informations permettant de créer la livraison
        __comments (List[str]) : commentaires à ajouter à la livraison
        __tags (Dict[str, str]) : tags à ajouter à la livraison
        __data_files (List[Path]): liste des fichiers de donnée à importer sur l'entrepôt.
        __md5_files (List[Path]): liste des fichiers md5 à importer sur l'entrepôt.
    """

    def __init__(self, d_dataset: Dict[Any, Any]) -> None:
        """Constructeur

        Args:
            d_dataset (Dict[Any, Any]): dataset tel que dans le fichier descriptif de livraison
        """
        # Définition des attributs
        self.__data_dirs: List[Path] = d_dataset["data_dirs"]
        self.__upload_infos: Dict[str, str] = d_dataset["upload_infos"]
        self.__comments: List[str] = d_dataset["comments"]
        self.__tags: Dict[str, str] = d_dataset["tags"]
        self.__data_files: Dict[Path, str] = {}
        self.__md5_files: List[Path] = []

        # Listing des fichiers de donnée à envoyer
        self.__list_data_files()
        # Génération des fichier md5 si nécessaire et listing
        self.__generate_md5_files()

    def __list_data_files(self) -> None:
        """Liste tous les fichiers de données à importer sur l'entrepôt API.
        Pour chaque fichier, au associe son Path local au chemin qui sera fourni à l'API.
        ex : Path(/root/dataset/data/fichier.shp) => "data"
        """
        raise NotImplementedError("Dataset.__list_data_files")

    def __generate_md5_files(self) -> None:
        """Génère les fichiers de clés md5 à importer sur l'entrepôt API.
        Pour chaque dossier de donnée, cherche un fichier .md5 correspondant,
        s'il n'existe pas il est créé et rempli en parcourant les fichiers enfants du dossier.
        S'il existe, rien n'est fait.
        """
        raise NotImplementedError("Dataset.__generate_md5_files")

    @property
    def data_dirs(self) -> List[Path]:
        return self.__data_dirs

    @property
    def upload_infos(self) -> Dict[str, str]:
        return self.__upload_infos

    @property
    def comments(self) -> List[str]:
        return self.__comments

    @property
    def tags(self) -> Dict[str, str]:
        return self.__tags

    @property
    def data_files(self) -> Dict[Path, str]:
        return self.__data_files

    @property
    def md5_files(self) -> List[Path]:
        return self.__md5_files
