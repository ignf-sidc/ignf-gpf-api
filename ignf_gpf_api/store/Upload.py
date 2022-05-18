from pathlib import Path
from typing import Any, Dict, List

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.TagInterface import TagInterface
from ignf_gpf_api.store.CommentInterface import CommentInterface
from ignf_gpf_api.store.SharingInterface import SharingInterface
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.Errors import StoreEntityError


class Upload(TagInterface, CommentInterface, SharingInterface, StoreEntity):
    """Classe Python représentant l'entité Upload (livraison)."""

    _entity_name = "upload"
    _entity_title = "livraison"

    def api_push_data_file(self, file_path: Path, api_path: str) -> None:
        """Envoie un fichier de donnée à la livraison.

        Args:
            file_path (Path): chemin local vers le fichier à envoyer
            api_path (str): dossier distant où déposer le fichier
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_push_data"

        # Ouverture du fichier et remplissage du tuple de fichier
        with file_path.open("rb") as o_file_binary:
            o_tuple_file = (file_path.name, o_file_binary)
            o_dict_files = {"file": o_tuple_file}
        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id},
            params={"path": api_path},
            files=o_dict_files,
        )

    def api_delete_data_file(self, api_path: str) -> None:
        """Supprime un fichier de donnée de la livraison.

        Args:
            api_path (str): chemin distant vers le fichier à supprimer
        """
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
        """Envoie un fichier md5 à la livraison.

        Args:
            file_path (Path): chemin local vers le fichier à envoyer
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_push_md5"

        # Ouverture du fichier et remplissage du tuple de fichier
        with file_path.open("rb") as o_file_binary:
            o_tuple_file = (file_path.name, o_file_binary)
            o_dict_files = {"file": o_tuple_file}
        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id},
            files=o_dict_files,
        )

    def api_delete_md5_file(self, api_path: str) -> None:
        """Supprime un fichier md5 de la livraison.

        Args:
            api_path (str): chemin distant vers le fichier à supprimer
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
        """Ouvre une livraison."""
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
        """Ferme une livraison."""
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
        """Test si la livraison est ouverte

        Returns:
            bool: si livraison ouverte
        """
        self.api_update()
        if "status" not in self._store_api_dict:
            raise StoreEntityError("Impossible de récupérer le status de l'upload")
        return bool(Config().get("upload_status", "open_status") == self["status"])

    def api_tree(self) -> List[Dict[str, Any]]:
        """Récupère l'arborescence d'une livraison."""
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
