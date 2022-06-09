from pathlib import Path
from typing import Any, Dict, List, Optional

from ignf_gpf_api.helper.JsonHelper import JsonHelper
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.io.Dataset import Dataset
from ignf_gpf_api.Errors import GpfApiError


class DescriptorFileReader:
    """Lit et valide le fichier descriptif d'un ensemble de datasets.

    Attributes :
        __descriptor_dict (Optional[Dict[Any, Any]]) : contenu du fichier descriptif
        __datasets (List[Dataset]): liste des datasets contenus dans le fichier descripteur de livraison
        __parent_folder(path): path du dossier parent des données
    """

    def __init__(self, descriptor_file_path: Path) -> None:
        """Constructeur

        Args:
            descriptor_file_path (Path): chemin vers le fichier descriptif de livraison
        """
        # Définition des attributs
        self.__descriptor_dict: Optional[Dict[Any, Any]] = None
        self.__datasets: List[Dataset] = []
        self.__parent_folder = descriptor_file_path.parent.absolute()
        # Ouverture du fichier descriptif de livraison
        self.__descriptor_dict = JsonHelper.load(descriptor_file_path, file_not_found_pattern="Fichier descriptif de livraison {json_path} non trouvé.")

        # Ouverture du schéma JSON à respecter
        p_schema_file_path = Config.conf_dir_path / Config().get("json_schemas", "descriptor_file")
        d_schema = JsonHelper.load(p_schema_file_path, file_not_found_pattern="Schéma de fichier descriptif de livraison {json_path} non trouvé. Contactez le support.")

        # Valide le fichier descriptif
        JsonHelper.validate_object(
            self.__descriptor_dict,
            d_schema,
            "Fichier descriptif de livraison {json_path} non valide.",
            "Schéma du fichier descriptif de livraison non valide. Contactez le support.",
        )

        # Vérification de l'existence des répertoires décrits dans le fichier
        self.__validate_pathes()
        # Vérification de l'existence des répertoires décrits dans le fichier et fabrication des chemins absolus à partir des chemins relatifs
        self.__instantiate_datasets()

    def __validate_pathes(self) -> None:
        """Vérifie si les répertoires existent (s'interrompt si l'un d'entre eux n'existe pas).

        Raises:
            GpfApiError : si un répertoire décrit dans le fichier descripteur n'existe pas
        """
        # liste qui va servir à lister les dossiers en erreurs
        l_liste_folder_non_valide: List[str] = []
        # On parcours la liste des datasets
        if self.__descriptor_dict is not None:
            for l_dataset in self.__descriptor_dict["datasets"]:
                # on parcours la liste des dossiers de chaque dataset
                for s_data_dir in l_dataset["data_dirs"]:
                    p_folder_path = self.__parent_folder / s_data_dir
                    if not p_folder_path.exists():
                        l_liste_folder_non_valide.append(str(p_folder_path))
            # si à la fin du parcours des dossiers la liste n'est pas vide, on lève une erreur:
            if l_liste_folder_non_valide:
                # affiche la liste des dossiers non valides
                Config().om.error("Liste des dossiers à téléverser non existants :\n  * {}".format("\n  * ".join(l_liste_folder_non_valide)))
                raise GpfApiError("Au moins un des répertoires listés dans le fichier descripteur de livraison n'existe pas.")

    def __instantiate_datasets(self) -> None:
        """Instancie les datasets."""
        if self.__descriptor_dict is not None:
            self.__datasets = [Dataset(i, self.__parent_folder) for i in self.__descriptor_dict["datasets"]]

    @property
    def datasets(self) -> List[Dataset]:
        return self.__datasets
