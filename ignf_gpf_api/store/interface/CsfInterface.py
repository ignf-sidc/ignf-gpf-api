from datetime import datetime
from typing import Optional

from ignf_gpf_api.store.StoreEntity import StoreEntity


class CsfInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les entités ayant une date de création,
    de démarrage et de fin (`creation`, `start` `finish` => CSF).
    """

    @property
    def creation(self) -> Optional[datetime]:
        """Récupère la datetime de création de l'entité.

        Returns:
            datetime: datetime de création de l'entité
        """
        return self._get_datetime("creation")

    @property
    def start(self) -> Optional[datetime]:
        """Récupère la datetime de début de l'entité.

        Returns:
            datetime: datetime de début de l'entité
        """
        return self._get_datetime("start")

    @property
    def finish(self) -> Optional[datetime]:
        """Récupère la datetime de fin de l'entité.

        Returns:
            datetime: datetime de fin de l'entité
        """
        return self._get_datetime("finish")
