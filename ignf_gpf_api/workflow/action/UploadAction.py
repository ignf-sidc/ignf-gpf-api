import time
from typing import Any, Callable, Dict, List, Optional


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
        Config().om.info("Création et complétion d'une livraison...")
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
        # Affiche et retourne la livraison
        if self.upload is not None:
            # Affichage
            Config().om.info(f"Livraison créée et complétée : {self.__upload}")
            Config().om.info("Création et complétion d'une livraison : terminé")
            # Retour
            return self.upload
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
            # On supprime/recrée la livraison si demandé
            if self.__behavior == "DELETE":
                Config().om.warning(f"Une livraison identique {o_upload} va être supprimée puis recréée...")
                o_upload.api_delete()
                # on en crée une nouvelle (on utilise les champs de "upload_infos" du dataset)
                self.__upload = Upload.api_create(self.__dataset.upload_infos)
                Config().om.warning(f"Livraison {self.__upload} recréée avec succès.")
            else:
                # Sinon on continue avec cet upload pour le compléter (behavior == CONTINUE)
                # cas livraison fermé : on plante
                if not o_upload.is_open():
                    raise GpfApiError(f"Impossible de continuer, la livraison {o_upload} est fermée.")
                Config().om.info(f"Livraison identique {o_upload} trouvée, le programme va la reprendre et la compléter.")
                self.__upload = o_upload
        else:
            # Si le livraison est nulle, on en crée une nouvelle (on utilise les champs de "upload_infos" du dataset)
            self.__upload = Upload.api_create(self.__dataset.upload_infos)
            Config().om.info(f"Livraison {self.__upload['name']} créée avec succès.")

    def __add_tags(self) -> None:
        """Ajoute les tags."""
        if self.__upload is not None and self.__dataset.tags is not None:
            Config().om.info(f"Livraison {self.__upload['name']} : ajout des {len(self.__dataset.tags)} tags...")
            self.__upload.api_add_tags(self.__dataset.tags)
            Config().om.info(f"Livraison {self.__upload['name']} : les {len(self.__dataset.tags)} tags ont été ajoutés avec succès.")

    def __add_comments(self) -> None:
        """Ajoute les commentaires."""
        if self.__upload is not None:
            Config().om.info(f"Livraison {self.__upload['name']} : ajout des {len(self.__dataset.comments)} commentaires...")
            for s_comment in self.__dataset.comments:
                self.__upload.api_add_comment({"text": s_comment})
            Config().om.info(f"Livraison {self.__upload['name']} : les {len(self.__dataset.comments)} commentaires ont été ajoutés avec succès.")

    def __push_data_files(self) -> None:
        """Téléverse les fichiers de données."""
        if self.__upload is not None:
            Config().om.info(f"Livraison {self.__upload['name']} : téléversement des {len(self.__dataset.data_files)} fichiers de données...")
            for p_file_path, s_api_path in self.__dataset.data_files.items():
                self.__upload.api_push_data_file(p_file_path, s_api_path)
            Config().om.info(f"Livraison {self.__upload['name']} : les {len(self.__dataset.data_files)} fichiers de données ont été téléversés avec succès.")

    def __push_md5_files(self) -> None:
        """Téléverse les fichiers de clefs."""
        if self.__upload is not None:
            Config().om.info(f"Livraison {self.__upload['name']} : téléversement des {len(self.__dataset.md5_files)} fichiers de clefs...")
            for p_file_path in self.__dataset.md5_files:
                self.__upload.api_push_md5_file(p_file_path)
            Config().om.info(f"Livraison {self.__upload['name']} : les {len(self.__dataset.md5_files)} fichiers de clefs ont été téléversés avec succès.")

    def __close(self) -> None:
        """Ferme la livraison."""
        if self.__upload is not None:
            Config().om.info(f"Livraison {self.__upload['name']} : fermeture de la livraison...")
            self.__upload.api_close()
            Config().om.info(f"Livraison {self.__upload['name']} : livraison fermée avec succès. La livraison va maintenant être vérifiée par la Géoplateforme.")

    def __find(self) -> Optional[Upload]:
        """Fonction permettant de lister un éventuel upload déjà existant à partir des critères d'unicité donnés.

        Returns:
            Optional[Upload]: None si rien trouvé, sinon l'Upload trouvé
        """
        # On tente de récupérer l'upload selon les critères d'attributs donnés en conf (uniqueness_constraint_infos)
        l_attributes = Config().get("upload_creation", "uniqueness_constraint_infos").split(";")
        d_attributs = {}
        for s_attribut in l_attributes:
            if s_attribut != "":
                d_attributs[s_attribut] = self.__dataset.upload_infos[s_attribut]
        # On tente de récupérer l'upload selon les critères de tags donnés en conf (uniqueness_constraint_tags)
        l_tags = Config().get("upload_creation", "uniqueness_constraint_tags").split(";")
        d_tags = {}
        for s_tag in l_tags:
            if s_tag != "":
                d_tags[s_tag] = self.__dataset.tags[s_tag]
        # On peut maintenant filter les upload selon ces critères
        l_uploads = Upload.api_list(infos_filter=d_attributs, tags_filter=d_tags)
        # S'il y a un ou plusieurs upload, on retourne le 1er :
        if l_uploads:
            return l_uploads[0]
        # sinon on retourne None
        return None

    @property
    def upload(self) -> Optional[Upload]:
        return self.__upload

    @staticmethod
    def monitor_until_end(upload: Upload, callback: Optional[Callable[[str], None]] = None) -> bool:
        """Attend que toute les vérifications liées à la Livraison indiquée soient terminées (en erreur ou en succès) avant de rendre la main.
        La fonction callback indiquée est exécutée en prenant en paramètre un message de suivi du nombre de vérifications par statut.

        Args:
            upload (Upload): Livraison à monitorer
            callback (Optional[Callable[[str], None]]): fonction de callback à exécuter avec le message de suivi. Defaults to None.

        Returns:
            bool: True si toutes les vérifications sont ok, sinon False
        """
        i_nb_sec_between_check = Config().get_int("upload_creation", "nb_sec_between_check_updates")
        s_check_message_pattern = Config().get("upload_creation", "check_message_pattern")
        b_success: Optional[bool] = None
        Config().om.info(f"Monitoring des vérifications toutes les {i_nb_sec_between_check} secondes...")
        while b_success is None:
            # On récupère les vérifications
            d_checks = upload.api_list_checks()
            # On peut déterminer b_success s'il n'y en a plus en attente et en cours
            if len(d_checks["asked"]) == len(d_checks["in_progress"]) == 0:
                b_success = len(d_checks["failed"]) == 0
            # On affiche un rapport via la fonction de callback précisée
            s_message = s_check_message_pattern.format(
                nb_asked=len(d_checks["asked"]),
                nb_in_progress=len(d_checks["in_progress"]),
                nb_passed=len(d_checks["passed"]),
                nb_failed=len(d_checks["failed"]),
            )
            if callback is not None:
                callback(s_message)
            # Si l'état est toujours indéterminé
            if b_success is None:
                # On attend le temps demandé
                time.sleep(i_nb_sec_between_check)
        # On log le dernier rapport selon l'état et on sort
        if b_success:
            Config().om.info(s_message)
            return True
        Config().om.warning(s_message)
        return False

    @staticmethod
    def parse_tree(tree: List[Dict[str, Any]], prefix: str = "") -> Dict[str, int]:
        """Parse l'arborescence renvoyée par l'API en un dictionnaire associant le chemin de chaque fichier à sa taille.
        L'objectif est de permettre de facilement identifier quel sont les fichiers à (re)livrer.
        Args:
            tree (List[Dict[str, Any]]): arborescence à parser
            prefix (str): pré-fixe du chemin
        Returns:
            Dict[str, int]: liste des fichiers envoyés et leur taille
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
                d_sub_files = UploadAction.parse_tree(d_element["children"], prefix=s_chemin)
                # On fusionne ces fichiers à notre dict principal
                d_files = {**d_files, **d_sub_files}
            else:
                raise GpfApiError(f"Type d'élément rencontré dans l'arborescence '{d_element['type']}' non géré. Contacter le support.")
        return d_files
