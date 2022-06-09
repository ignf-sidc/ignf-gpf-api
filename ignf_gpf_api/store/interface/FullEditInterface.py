from typing import Dict
from ignf_gpf_api.store.StoreEntity import StoreEntity


class FullEditInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les étiquettes (tags)."""

    def api_full_edit(self, data_edit: Dict[str, str]) -> None:
        """Modifie complètement l'entité sur l'API (PUT).

        Args:
            data_edit (Dict[str, str]): nouvelles valeurs de propriétés
        """
        raise NotImplementedError(f"FullEditInterface.api_full_edit({data_edit})")
