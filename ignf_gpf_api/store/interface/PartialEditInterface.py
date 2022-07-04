from typing import Dict
from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.io.ApiRequester import ApiRequester


class PartialEditInterface(StoreEntity):
    """Interface de StoreEntity pour gérer l'édition partielle de l'entité."""

    def api_partial_edit(self, d_data_edit: Dict[str, str]) -> None:
        """Modifie partiellement l'entité sur l'API (PATCH).

        Args:
            d_data_edit (Dict[str, str]): nouvelles valeurs pour les propriétés à modifier
        """
        # Requête
        ApiRequester().route_request(
            f"{self._entity_name}_partial_edit",
            data=d_data_edit,
            method=ApiRequester.PATCH,
            route_params={self._entity_name: self.id},
        )

        # Mise à jour du stockage local (_store_api_dict)
        self.api_update()
