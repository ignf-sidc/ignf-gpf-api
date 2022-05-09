from typing import Any, Dict, List
from ignf_gpf_api.store.StoreEntity import StoreEntity


class CommentInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les commentaires."""

    def api_add_comment(self, comment_data: Dict[str, str]) -> None:
        """Ajout un commentaire à l'entité.

        Args:
            comment_data (Dict[str, str]): données du commentaire
        """
        raise NotImplementedError("CommentInterface.api_add_comment")

    def api_list_comments(self) -> List[Dict[str, Any]]:
        """Liste les commentaires de l'entité.

        Returns:
            List[Dict[str, Any]]: liste des commentaires
        """
        raise NotImplementedError("CommentInterface.api_edit_comment")

    def api_edit_comment(self, id_: str, comment_data: str) -> None:
        """Modifie un commentaire de l'entité.

        Args:
            id_ (str): identifiant du commentaire
            comment_data (Dict[str, str]): données du commentaire
        """
        raise NotImplementedError("CommentInterface.api_edit_comment")

    def api_remove_comment(self, id_: str) -> None:
        """Supprime un commentaire de l'entité.

        Args:
            id_ (str): identifiant du commentaire
        """
        raise NotImplementedError("CommentInterface.api_remove_comment")
