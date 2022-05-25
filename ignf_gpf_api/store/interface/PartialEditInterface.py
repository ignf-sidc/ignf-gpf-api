from typing import Dict
from ignf_gpf_api.store.StoreEntity import StoreEntity


class PartialEditInterface(StoreEntity):
    """Interface de StoreEntity pour gérer l'édition partielle de l'entité."""

    def api_partial_edit(self, d_data_edit: Dict[str, str]) -> None:
        """Modifie partiellement l'entité sur l'API (PATCH).

        Args:
            d_data_edit (Dict[str, str]): nouvelles valeurs pour les propriétés à modifier
        """
        raise NotImplementedError(f"PartialEditInterface.api_partial_edit({d_data_edit})")
