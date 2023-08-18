from abc import ABC
from typing import Type, Optional, Any, Dict, TypeVar
from ignf_gpf_api.store.Errors import StoreEntityError

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.DownloadInterface import DownloadInterface

T = TypeVar("T", bound="StoreEntity")


class AbstractCommonFile(DownloadInterface, StoreEntity, ABC):
    """Classe abstraite Python pour les Fichiers communs."""

    _entity_name = "common_file"
    _entity_title = "Fichiers communs"

    # neutralisation de l'ajout et de la suppression

    @classmethod
    def api_create(cls: Type[T], data: Optional[Dict[str, Any]], route_params: Optional[Dict[str, Any]] = None) -> T:
        """Crée une nouvelle entité dans l'API.

        Args:
            data: Données nécessaires pour la création.
            route_params: Paramètres de résolution de la route.

        Returns:
            (StoreEntity): Entité créée
        """
        raise StoreEntityError(f"Impossible de créer un {cls.entity_title()}.")

    def api_delete(self) -> None:
        """Supprime l'entité de l'API."""
        raise StoreEntityError(f"Impossible de supprimer un {self.entity_title()}.")
