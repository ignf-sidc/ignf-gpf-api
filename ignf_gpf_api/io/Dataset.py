from pathlib import Path
from typing import Any, Dict, List
from ignf_gpf_api.helper.FileHelper import FileHelper

from ignf_gpf_api.io.Config import Config


class Dataset:
    """Classe portante les infos nécessaires à la création d'une livraison et issues du dataset.

    Attributes :
        __data_dirs (List[Path]) : liste des dossiers à envoyer à l'API
        __upload_infos (Dict[str, str]) : informations permettant de créer la livraison
        __comments (List[str]) : commentaires à ajouter à la livraison
        __tags (Dict[str, str]) : tags à ajouter à la livraison
        __data_files (List[Path]): liste des fichiers de donnée à importer sur l'entrepôt.
        __md5_files (List[Path]): liste des fichiers md5 à importer sur l'entrepôt.
        __root_dir (Path): Chemin racine du dataset (absolu ou relatif ?)
    """

    def __init__(self, dataset: Dict[Any, Any], p_root_dir: Path) -> None:
        """Constructeur

        Args:
            dataset (Dict[Any, Any]): dataset tel que dans le fichier descriptif de livraison
            p_root_dir (Path): Chemin racine à partir duquel sont défini les data_dirs
        """
        # Définition des attributs
        self.__data_dirs: List[Path] = [Path(i) for i in dataset["data_dirs"]]  # Chemins relatifs
        self.__upload_infos: Dict[str, str] = dataset["upload_infos"]
        self.__comments: List[str] = dataset["comments"]
        self.__tags: Dict[str, str] = dataset["tags"]
        self.__data_files: Dict[Path, str] = {}
        self.__md5_files: List[Path] = []
        self.__root_dir: Path = p_root_dir

        # Listing des fichiers de donnée à envoyer
        self.__list_data_files()
        # Génération des fichier md5 si nécessaire et listing
        self.__generate_md5_files()

    def __list_data_files(self) -> None:
        """Liste tous les fichiers de données à importer sur l'entrepôt API.
        Pour chaque fichier, on associe son Path local au chemin qui sera fourni à l'API.
        ex : Path(/root/dataset/data/fichier.shp) => "dataset/data"
        """
        p_abs_root_dir = self.__root_dir.absolute()
        for p_dir in self.__data_dirs:
            self.__list_rec(p_abs_root_dir, p_dir)

    def __generate_md5_files(self) -> None:
        """Génère les fichiers de clés md5 à importer sur l'entrepôt API.
        Pour chaque dossier de donnée, cherche un fichier .md5 correspondant,
        s'il n'existe pas il est créé et rempli en parcourant les fichiers enfants du dossier.
        S'il existe, rien n'est fait.
        """
        p_abs_root_dir = self.__root_dir.absolute()
        s_pattern = Config().get("upload_creation", "md5_pattern")

        # On parcourt le dictionnaire des répertoires
        for p_dir in self.__data_dirs:
            p_md5_dir = Path(p_abs_root_dir / p_dir)
            p_md5_dir_suf = p_md5_dir.with_suffix(".md5")

            # On teste si le fichier md5 existe, sinon on le crée
            if not p_md5_dir_suf.exists():
                Config().om.info(f"Le fichier md5 {p_md5_dir_suf.relative_to(self.__root_dir)} n'existe pas, il va être créé")

                # On parcourt les fichiers pour remplir un dictionnaire temporaire
                d_md5 = {}
                for p_file in self.__data_files:
                    if p_md5_dir in p_file.parents:
                        p_file_trunc = p_file.relative_to(self.__root_dir)
                        d_md5[p_file_trunc] = FileHelper.md5_hash(p_file)

                # A la fin on rempli le fichier .md5
                with open(p_md5_dir_suf, "w", encoding="utf-8") as o_md5_file:
                    for p_file, s_md5 in d_md5.items():
                        o_md5_file.write(f"{s_pattern}\n".format(md5_key=s_md5, file_path=p_file))

            # Enfin, on l'ajoute à la liste des fichiers md5
            self.__md5_files.append(p_md5_dir_suf)

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

    def __list_rec(self, root_dir: Path, path_rep: Path) -> None:
        """
        Fonction récursive permettant de lister des fichiers

        Args:
            root_dir (Path): Chemin absolu du dossier racine
            path_rep (Path): Chemin du dossier à lister
        """

        p_rep = root_dir / path_rep
        l_elt = p_rep.iterdir()

        for p_elt in l_elt:
            p_rep_elt = path_rep / p_elt
            # Appel récursif si l'élément est un dossier
            if p_elt.is_dir():
                self.__list_rec(p_rep, Path(p_elt.name))
            # L'élément est un fichier
            elif p_elt.is_file():
                # Création du chemin relatif pour l'API
                p_api = p_rep_elt.relative_to(self.__root_dir)
                # Remplissage du dictionnaire __data_files
                self.__data_files[p_rep_elt] = str(p_api.parent)
