from typing import Dict, List

from ignf_gpf_api.store.StoreEntity import StoreEntity


class SharingInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les partages."""

    def api_add_sharings(self, datastore_ids: List[str]) -> None:
        """Partage l'entité avec les datastore indiqués.

        Args:
            datastore_ids (List[str]): liste des identifiants des datastore avec qui partager l'entité
        """
        raise NotImplementedError("SharingInterface.api_add_sharings")

    def api_list_sharings(self) -> List[Dict[str, str]]:
        """Liste les datastore avec lesquels l'entité est partagée.

        Returns:
            List[Dict[str, str]]: Liste des datastore {id_ et name}
        """
        raise NotImplementedError("SharingInterface.api_list_sharings")

    def api_remove_sharings(self, datastore_ids: List[str]) -> None:
        """Arrête le partage de l'entité avec les datastore indiqués.

        Args:
            datastore_ids (List[str]): liste des identifiants des datastore avec qui arrêter de partager l'entité
        """
        raise NotImplementedError("SharingInterface.api_remove_sharings")
