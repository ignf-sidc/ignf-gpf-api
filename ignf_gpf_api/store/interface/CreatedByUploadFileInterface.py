from pathlib import Path
from typing import Any, Dict, Optional, Type, TypeVar
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.Errors import StoreEntityError
from ignf_gpf_api.store.StoreEntity import StoreEntity

T = TypeVar("T", bound="StoreEntity")


class CreatedByUploadFileInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les entités créer par l'upload d'un fichier."""

    @classmethod
    def api_create(cls: Type[T], data: Optional[Dict[str, Any]], route_params: Optional[Dict[str, Any]] = None) -> T:
        """Crée une nouvelle entité dans l'API.

        Args:
            data: Données nécessaires pour la création. Dont "file": Path("chemin fichier") et "api_path": "nom fichier"
            route_params: Paramètres de résolution de la route.

        Returns:
            (StoreEntity): Entité créée
        """
        s_datastore: Optional[str] = None
        # Test du dictionnaire route_params
        if isinstance(route_params, dict) and "datastore" in route_params:
            s_datastore = route_params.get("datastore")

        # Génération du nom de la route
        s_route = f"{cls._entity_name}_upload"

        # récupération du ficher et du nom du ficher après livraison
        if not data or "file" not in data or "api_path" not in data:
            raise StoreEntityError('Entité créée par l\'upload d\'un fichier, les clefs "file": Path("chemin fichier") et "api_path": "nom fichier" sont obligatoires dans data')
        p_file = Path(data.pop("file"))
        s_api_path = data.pop("api_path")

        # nom de la clef dans le fichier
        s_file_key = Config().get_str(cls.entity_name(), "create_file_key")

        # Requête
        o_response = ApiRequester().route_upload_file(
            s_route,
            p_file,
            s_file_key,
            route_params=route_params,
            params={"path": s_api_path},
            method=ApiRequester.POST,
            data=data,
        )

        # Instanciation
        return cls(o_response.json(), datastore=s_datastore)
