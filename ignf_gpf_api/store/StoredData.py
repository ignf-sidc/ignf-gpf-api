from typing import Dict

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.TagInterface import TagInterface
from ignf_gpf_api.store.EventInterface import EventInterface
from ignf_gpf_api.store.CommentInterface import CommentInterface
from ignf_gpf_api.store.SharingInterface import SharingInterface


class StoredData(TagInterface, CommentInterface, SharingInterface, EventInterface, StoreEntity):
    """Classe Python représentant l'entité StoredData (donnée stockée)."""

    _entity_name = "stored_data"
    _entity_title = "donnée stockée"

    def api_edit(self, d_data_edit: Dict[str, str]) -> None:
        """Modifie une donnée stockée sur l'API.

        Args:
            d_data_edit (Dict[str, str]): nouvelles valeurs pour les propriétés à modifier
        """
        raise NotImplementedError(f"StoredData.api_edit({d_data_edit})")
