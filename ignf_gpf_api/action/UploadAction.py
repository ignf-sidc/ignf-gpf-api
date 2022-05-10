from typing import Optional


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
        # On suit le comporte donnée en paramètre ou à défaut celui de la config
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
            if self.__behavior == "STOP":
                raise GpfApiError(f"Impossible de créer la livraison, une livraison identique {o_upload} existe déjà.")
            # On supprime la livraison si demandé
            if self.__behavior == "DELETE":
                Config().om.warning(f"Une livraison identique {o_upload} va être supprimée.")
                o_upload.api_delete()
            # Sinon on continue avec cet upload pour le compléter (behavior == CONTINUE)
            Config().om.info(f"Livraison identique {o_upload} trouvée, le programme va reprendre et la compléter.")
            self.__upload = o_upload
        else:
            # Si l'upload est nul, on en crée un nouveau
            self.__upload = Upload.api_create(self.__dataset.upload_infos)
            Config().om.info(f"Livraison {o_upload} créée avec succès.")

    def __add_tags(self) -> None:
        """Ajout les tags."""

    def __add_comments(self) -> None:
        """Ajout les commentaires."""

    def __push_data_files(self) -> None:
        """Envoie les fichiers de données."""

    def __push_md5_files(self) -> None:
        """Envoie les fichiers md5."""

    def __close(self) -> None:
        """Ferme la livraison."""

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
