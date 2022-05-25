from typing import Any, Dict, List

from ignf_gpf_api.store.StoreEntity import StoreEntity


class EventInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les événement."""

    def api_events(self) -> List[Dict[str, Any]]:
        """Liste les événements associés à l'entité."""
        raise NotImplementedError("EventInterface.api_events")
