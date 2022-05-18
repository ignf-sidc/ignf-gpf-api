from typing import Any, Dict, List
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.StoreEntity import StoreEntity


class CommentInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les commentaires."""

    def api_add_comment(self, comment_data: Dict[str, str]) -> None:
        """Ajout un commentaire à l'entité.

        Args:
            comment_data (Dict[str, str]): données du commentaire
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_add_comment"
        # Requête "get"
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id},
            data=comment_data,
        )

    def api_list_comments(self) -> List[Dict[str, Any]]:
        """Liste les commentaires de l'entité.

        Returns:
            List[Dict[str, Any]]: liste des commentaires
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_list_comment"
        # Requête "get"
        o_response = ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id},
        )
        l_comments: List[Dict[str, Any]] = o_response.json()
        return l_comments

    def api_edit_comment(self, id_: str, comment_data: Dict[str, str]) -> None:
        """Modifie un commentaire de l'entité.

        Args:
            id_ (str): identifiant du commentaire
            comment_data (Dict[str, str]): données du commentaire
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_edit_comment"
        # Requête "post"
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.PUT,
            route_params={self._entity_name: self.id, "comment": id_},
            data=comment_data,
        )

    def api_remove_comment(self, id_: str) -> None:
        """Supprime un commentaire de l'entité.

        Args:
            id_ (str): identifiant du commentaire
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_remove_comment"
        # Requête "delete"
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.DELETE,
            route_params={self._entity_name: self.id, "comment": id_},
        )
