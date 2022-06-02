from typing import Any, Dict, List

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.io.ApiRequester import ApiRequester


class EventInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les événement."""

    def api_events(self) -> List[Dict[str, Any]]:
        """Liste les événements.

        Returns:
            List[Dict[str, Any]]: liste des événements
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_list_event"
        # Requête "get" à l'API
        o_response = ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id},
        )
        l_events: List[Dict[str, Any]] = o_response.json()
        return l_events
