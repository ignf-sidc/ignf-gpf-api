from typing import Any, Dict, List, Optional


from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.store.Upload import Upload
from ignf_gpf_api.io.Dataset import Dataset
from ignf_gpf_api.io.Config import Config


class UploadAction:
    """Classe permettant d'accompagner la création d'une livraison.

    Attributes :
        __dataset (Dataset): dataset contenant les info de la livraison à créer
        __upload (Optional[Upload]): livraison représentant l'entité créée sur l'entrepôt
        __behavior (str): comportement à adopter si la livraison existe déjà sur l'entrepôt
    """

    BEHAVIOR_STOP = "STOP"
    BEHAVIOR_DELETE = "DELETE"
    BEHAVIOR_CONTINUE = "CONTINUE"

    def __init__(self, dataset: Dataset, behavior: Optional[str] = None) -> None:
        self.__dataset: Dataset = dataset
        self.__upload: Optional[Upload] = None
        # On suit le comportement donnée en paramètre ou à défaut celui de la config
        self.__behavior: str = behavior if behavior is not None else Config().get("upload_creation", "behavior_if_exists")

    def run(self) -> Upload:
        """Crée la livraison décrite dans le dataset et livre les données avant de
        retourner la livraisons crée.

        Returns:
            Upload: livraison créée
        """
        # Création de la livraison
        self.__create_upload()
        # Ajout des tags
        self.__add_tags()
        # Ajout des commentaires
        self.__add_comments()
        # Envoie des fichiers de données
        self.__push_data_files()
        # Envoie des fichiers md5
        self.__push_md5_files()
        # Fermeture de la livraison
        self.__close()
        # Retourne la liste de livraisons
        if self.__upload is not None:
            return self.__upload
        # On ne devrait pas arriver ici...
        raise GpfApiError("Erreur à la création de la livraison.")

    def __create_upload(self) -> None:
        """Crée l'upload après avoir vérifié s'il n'existe pas déjà..."""
        Config().om.info("Création d'une livraison...")
        # On tente de récupérer l'upload
        o_upload = self.__find()
        # S'il n'est pas null
        if o_upload is not None:
            # On sort en erreur si demandé
            if self.__behavior == self.BEHAVIOR_STOP:
                raise GpfApiError(f"Impossible de créer la livraison, une livraison identique {o_upload} existe déjà.")
            # On recrée la livraison si demandé
            if self.__behavior == self.BEHAVIOR_DELETE:
                Config().om.warning(f"Une livraison identique {o_upload} va être supprimée puis recréée")
                o_upload.api_delete()
                # on en crée un nouveau
                self.__upload = Upload.api_create(self.__dataset.upload_infos)
            else:
                # Sinon on continue avec cet upload pour le compléter (behavior == self.BEHAVIOR_CONTINUE)
                # cas livraison fermée : on plante
                if not o_upload.is_open():
                    raise GpfApiError(f"Impossible de continué, la livraison {o_upload} est fermée.")
                Config().om.info(f"Livraison identique {o_upload} trouvée, le programme va reprendre et la compléter.")
                self.__upload = o_upload
        else:
            # Si l'upload est nul, on en crée un nouveau
            self.__upload = Upload.api_create(self.__dataset.upload_infos)
            Config().om.info(f"Livraison {self.__upload} créée avec succès.")

    def __add_tags(self) -> None:
        """Ajout les tags."""
        if self.__upload is not None and self.__dataset.tags is not None:
            self.__upload.api_add_tags(self.__dataset.tags)
            Config().om.info(f"Livraison {self.__upload}: les {len(self.__dataset.tags)} tags ont été ajoutés avec succès.")

    def __add_comments(self) -> None:
        """Ajout les commentaires."""
        if self.__upload is not None:
            for s_comment in self.__dataset.comments:
                self.__upload.api_add_comment({"text": s_comment})
            Config().om.info(f"Livraison {self.__upload}: les {len(self.__dataset.comments)} commentaires ont été ajoutés avec succès.")

    def __push_data_files(self) -> None:
        """Envoie les fichiers de données (listés dans le dataset)."""
        if self.__upload is not None:
            # lister les fichiers uploadés de l'entrepot et récupérer leur taille (sur l'entrepot)
            l_arborescence = self.__upload.api_tree()
            d_destination_taille = UploadAction.parse_tree(l_arborescence)

            for p_file_path, s_api_path in self.__dataset.data_files.items():
                # regarder si le fichier du dataset est deja dans la liste des fichiers uploadés sur l'entrepot
                # NB: sur l'entrepot, tous les fichiers "data" sont dans le dossier parent "data"
                s_data_api_path = f"data/{s_api_path}"
                if s_data_api_path in d_destination_taille:
                    # le fichier est deja livré, on check sa taille :
                    if d_destination_taille[s_data_api_path] == p_file_path.stat().st_size:
                        # le fichier a été complètement téléversé. On passe au fichier suivant.
                        continue

                    # le fichier n'a pas été téléversé en totalité.
                    # Si le mode "Append" n'est pas disponible sur le serveur, il faut supprimer le fichier à moitié uploadé.
                    # Sinon il faudra reprendre le téléversement (!)
                    self.__upload.api_delete_data_file(s_data_api_path)

                # sinon, on doit livrer le fichier
                self.__upload.api_push_data_file(p_file_path, s_api_path)
            Config().om.info(f"Livraison {self.__upload}: les {len(self.__dataset.data_files)} fichiers de données ont été ajoutés avec succès.")

    def __push_md5_files(self) -> None:
        """Envoie les fichiers md5 (listés dans le dataset)."""
        if self.__upload is not None:
            # lister les fichiers md5 uploadés de l'entrepot et récupérer leur taille (sur l'entrepot)
            l_arborescence = self.__upload.api_tree()
            d_destination_taille = UploadAction.parse_tree(l_arborescence)

            for p_file_path in self.__dataset.md5_files:
                # regarder si le fichier du dataset est deja dans la liste des fichiers uploadés sur l'entrepot
                # NB: sur l'entrepot, tous les fichiers md5 sont à la racine
                s_api_path = p_file_path.name
                if s_api_path in d_destination_taille:
                    # le fichier est deja livré, on check sa taille :
                    if d_destination_taille[s_api_path] == p_file_path.stat().st_size:
                        # le fichier a été complètement téléversé. On passe au fichier suivant.
                        continue

                    # le fichier n'a pas été téléversé en totalité.
                    # Si le mode "Append" n'est pas disponible sur le serveur, il faut supprimer le fichier à moitié uploadé.
                    # Sinon il faudra reprendre le téléversement (!)
                    self.__upload.api_delete_data_file(s_api_path)

                # sinon, on doit livrer le fichier
                self.__upload.api_push_md5_file(p_file_path)
            Config().om.info(f"Livraison {self.__upload}: les {len(self.__dataset.md5_files)} fichiers md5 ont été ajoutés avec succès.")

    def __close(self) -> None:
        """Ferme la livraison."""
        if self.__upload is not None:
            self.__upload.api_close()
            Config().om.info(f"Livraison {self.__upload} créée avec succès")

    def __find(self) -> Optional[Upload]:
        """Fonction permettant de lister un éventuel upload déjà existant à partir des critères d'unicité donnés.

        Returns:
            Optional[Upload]: None si rien trouvé, sinon l'Upload trouvé
        """
        # On tente de récupérer l'upload selon les critères d'attributs donnés en conf (uniqueness_constraint_upload_infos)
        l_attributes = Config().get("upload_creation", "uniqueness_constraint_upload_infos").split(";")
        d_attributs = {}
        for s_attribut in l_attributes:
            if s_attribut != "":
                d_attributs[s_attribut] = self.__dataset.upload_infos[s_attribut]
        # On tente de récupérer l'upload selon les critères de tags donnés en conf (uniqueness_constraint_tags)
        l_tags = Config().get("upload_creation", "uniqueness_constraint_tags").split(";")
        d_tags = {}
        for s_tag in l_tags:
            if s_tag != "":
                d_tags[s_tag] = self.__dataset.upload_infos[s_tag]
        # On peut maintenant filter les upload selon ces critères
        l_uploads = Upload.api_list(infos_filter=d_attributs, tags_filter=d_tags)
        # S'il y a un ou plusieurs upload, on retourne le 1er :
        if l_uploads:
            return l_uploads[0]
        # sinon on retourne None
        return None

    @staticmethod
    def parse_tree(tree: List[Dict[str, Any]], prefix: str = "") -> Dict[str, int]:
        """Parse l'arborescence renvoyée par l'API en un dictionnaire associant le chemin de chaque fichier à sa taille.
        L'objectif est de permettre de facilement identifier quel sont les fichiers à (re)livrer.
        Args:
            tree (List[Dict[str, Any]]): arborescence à parser (coté destination sur l'API)
            prefix (str): pré-fixe du chemin
        Returns:
            Dict[str, int]: liste des fichiers déjà sur la Destination et leur taille
        """
        # Création du dictionnaire pour stocker les fichiers et leur taille
        d_files: Dict[str, int] = {}
        # Parcours de l'arborescence
        for d_element in tree:
            # On complète le chemin
            if prefix != "":
                s_chemin = f"{prefix}/{d_element['name']}"
            else:
                s_chemin = str(d_element["name"])
            # Fichier ou dossier ?
            if d_element["type"] == "file":
                # Fichier, on l'ajoute à notre dictionnaire
                d_files[s_chemin] = int(d_element["size"])
            elif d_element["type"] == "directory":
                # Dossier, on itère dessus avec le nom du dossier comme préfixe
                d_subfiles = UploadAction.parse_tree(d_element["children"], prefix=s_chemin)
                # On fusionne ces fichiers à notre dict principal
                d_files = {**d_files, **d_subfiles}
            else:
                raise GpfApiError(f"Type d'élément rencontré dans l'arborescence '{d_element['type']}' non géré. Contacter le support.")
        return d_files
