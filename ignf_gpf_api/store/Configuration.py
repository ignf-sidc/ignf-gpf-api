from typing import Any, Dict, List

from ignf_gpf_api.store.Offering import Offering
from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.TagInterface import TagInterface
from ignf_gpf_api.store.interface.CommentInterface import CommentInterface
from ignf_gpf_api.store.interface.EventInterface import EventInterface
from ignf_gpf_api.store.interface.FullEditInterface import FullEditInterface


class Configuration(TagInterface, CommentInterface, EventInterface, FullEditInterface, StoreEntity):
    """Classe Python représentant l'entité Configuration (configuration)."""

    _entity_name = "configuration"
    _entity_title = "configuration"

    STATUS_UNPUBLISHED = "UNPUBLISHED"
    STATUS_PUBLISHED = "PUBLISHED"
    STATUS_SYNCHRONIZING = "SYNCHRONIZING"

    def api_list_offerings(self) -> List[Offering]:
        """Liste les Offering liées à cette Configuration.

        Returns:
            List[Offering]: liste des Offering trouvées
        """
        raise NotImplementedError("Configuration.api_list_offerings")

    def api_add_offering(self, data_offering: Dict[str, Any]) -> Offering:
        """Ajoute une Offering à cette Configuration.

        Args:
            data_offering (Dict[str, Any]): données pour la création de l'Offering

        Returns:
            Offering: représentation Python de l'Offering créée
        """
        return Offering.api_create(data_offering, route_params={self._entity_name: self.id})
