from typing import Any, Dict, Optional, Type, TypeVar
from ignf_gpf_api.store.Errors import StoreEntityError

from ignf_gpf_api.store.StoreEntity import StoreEntity


T = TypeVar("T", bound="StoreEntity")


class User(StoreEntity):
    """Classe Python représentant l'entité User (utilisateur)."""

    _entity_name = "user"
    _entity_title = "utilisateur"

    @classmethod
    def api_create(cls: Type[T], data: Optional[Dict[str, Any]], route_params: Optional[Dict[str, Any]] = None) -> T:
        """Crée une nouvelle entité dans l'API.

        Args:
            data: Données nécessaires pour la création.
            route_params: Paramètres de résolution de la route.

        Returns:
            (StoreEntity): Entité créée
        """
        raise StoreEntityError(f"Impossible de créer un {cls.entity_title()}")

    def api_delete(self) -> None:
        """Supprime l'entité de l'API."""
        raise StoreEntityError(f"Impossible de supprimer un {self.entity_title()}")
