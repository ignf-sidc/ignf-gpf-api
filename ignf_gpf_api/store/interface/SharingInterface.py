from typing import Dict, List

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.io.ApiRequester import ApiRequester


class SharingInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les partages."""

    def api_add_sharings(self, datastore_ids: List[str]) -> None:
        """Partage l'entité avec les datastore indiqués.

        Args:
            datastore_ids (List[str]): liste des identifiants des datastore avec qui partager l'entité
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_add_sharings"
        # Requête "get"
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id},
            data=datastore_ids,
        )

    def api_list_sharings(self) -> List[Dict[str, str]]:
        """Liste les datastore avec lesquels l'entité est partagée.

        Returns:
            List[Dict[str, str]]: Liste des datastore {id_ et name}
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_list_sharings"
        # Requête "get"
        o_response = ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id},
        )
        l_sharings: List[Dict[str, str]] = o_response.json()

        return l_sharings

    def api_remove_sharings(self, datastore_ids: List[str]) -> None:
        """Arrête le partage de l'entité avec les datastore indiqués.

        Args:
            datastore_ids (List[str]): liste des identifiants des datastore avec qui arrêter de partager l'entité
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_remove_sharings"
        # Requête "delete"
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.DELETE,
            route_params={self._entity_name: self.id},
            params={"datastores[]": datastore_ids},
        )
