from pathlib import Path
from typing import Any, Dict, List

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.TagInterface import TagInterface
from ignf_gpf_api.store.interface.CommentInterface import CommentInterface
from ignf_gpf_api.store.interface.SharingInterface import SharingInterface
from ignf_gpf_api.store.interface.EventInterface import EventInterface
from ignf_gpf_api.store.interface.PartialEditInterface import PartialEditInterface
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.Errors import StoreEntityError


class Upload(TagInterface, CommentInterface, SharingInterface, EventInterface, PartialEditInterface, StoreEntity):
    """Classe Python représentant l'entité Upload (livraison).

    Cette classe permet d'effectuer les actions spécifiques liées aux livraisons : déclaration,
    téléversement, fermeture, gestion des vérifications, etc.
    """

    _entity_name = "upload"
    _entity_title = "livraison"

    STATUS_CREATED = "CREATED"
    STATUS_OPEN = "OPEN"
    STATUS_CLOSED = "CLOSED"
    STATUS_CHECKING = "CHECKING"
    STATUS_GENERATING = "GENERATING"
    STATUS_MODIFYING = "MODIFYING"
    STATUS_UNSTABLE = "UNSTABLE"
    STATUS_DELETED = "DELETED"

    def api_push_data_file(self, file_path: Path, api_path: str) -> None:
        """Téléverse via l'API un fichier de donnée associé à cette Livraison.

        Args:
            file_path: chemin local vers le fichier à envoyer
            api_path: chemin distant du dossier où déposer le fichier
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_push_data"
        # Récupération du nom de la clé pour le fichier
        s_file_key = Config().get("upload", "push_data_file_key")

        # Ouverture du fichier et remplissage du tuple de fichier
        with file_path.open("rb") as o_file_binary:
            o_tuple_file = (file_path.name, o_file_binary)
            o_dict_files = {s_file_key: o_tuple_file}
            # Requête
            ApiRequester().route_request(
                s_route,
                method=ApiRequester.POST,
                route_params={self._entity_name: self.id},
                params={"path": api_path},
                files=o_dict_files,
            )

    def api_delete_data_file(self, api_path: str) -> None:
        """Supprime un fichier de donnée de la Livraison.

        Retire `data/` de devant le chemin distant si jamais il le contient.

        Args:
            api_path: chemin distant vers le fichier à supprimer
        """
        # On retire data/ de devant le chemin si jamais il le contient
        if api_path.startswith("data/"):
            api_path = api_path[5:]

        # Génération du nom de la route
        s_route = f"{self._entity_name}_delete_data"

        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.DELETE,
            route_params={self._entity_name: self.id},
            params={"path": api_path},
        )

    def api_push_md5_file(self, file_path: Path) -> None:
        """Téléverse via l'API un fichier de clefs associé à cette Livraison.

        Args:
            file_path: chemin local vers le fichier à envoyer
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_push_md5"
        # Récupération du nom de la clé pour le fichier
        s_file_key = Config().get("upload", "push_md5_file_key")

        # Ouverture du fichier et remplissage du tuple de fichier
        with file_path.open("rb") as o_file_binary:
            o_tuple_file = (file_path.name, o_file_binary)
            o_dict_files = {s_file_key: o_tuple_file}
            # Requête
            ApiRequester().route_request(
                s_route,
                method=ApiRequester.POST,
                route_params={self._entity_name: self.id},
                files=o_dict_files,
            )

    def api_delete_md5_file(self, api_path: str) -> None:
        """Supprime un fichier de clefs de la Livraison.

        Args:
            api_path: chemin distant vers le fichier à supprimer
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_delete_md5"

        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.DELETE,
            route_params={self._entity_name: self.id},
            params={"path": api_path},
        )

    def api_open(self) -> None:
        """Ouvre la Livraison."""
        # Génération du nom de la route
        s_route = f"{self._entity_name}_open"

        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id},
        )

        # Mise à jour du stockage local (_store_api_dict)
        self.api_update()

    def api_close(self) -> None:
        """Ferme la livraison."""
        # Génération du nom de la route
        s_route = f"{self._entity_name}_close"

        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id},
        )

        # Mise à jour du stockage local (_store_api_dict)
        self.api_update()

    def is_open(self) -> bool:
        """Teste si la livraison est ouverte à partir des propriétés stockées en local.

        Returns:
            `True` si la Livraison est ouverte
        """
        self.api_update()
        if "status" not in self._store_api_dict:
            raise StoreEntityError("Impossible de récupérer le status de l'upload")
        return bool(Config().get("upload", "status_open") == self["status"])

    def api_tree(self) -> List[Dict[str, Any]]:
        """Récupère l'arborescence des fichiers téléversés associés à cette Livraison.

        Returns:
            Arborescence telle que renvoyée par l'API
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_tree"

        # Requête
        o_response = ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id},
        )

        # Retour de l'arborescence
        l_tree: List[Dict[str, Any]] = o_response.json()
        return l_tree

    def api_list_checks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Liste les Vérifications (Check) lancées sur cette livraison.

        Returns:
            Liste des Vérifications demandées (clef `asked`), en cours (`in_progress`), passées (`passed`) et en échec (`failed`)
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_list_checks"

        # Requête
        o_response = ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id},
        )

        d_list_checks: Dict[str, List[Dict[str, Any]]] = o_response.json()
        return d_list_checks

    def api_run_checks(self, check_ids: List[str]) -> None:
        """Lance des Vérifications (Check) supplémentaires sur cette Livraison.

        Args:
            check_ids: Liste des identifiants des Vérifications à lancer
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_run_checks"

        # Requête
        ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id},
            method=ApiRequester.POST,
            data=check_ids,
        )
