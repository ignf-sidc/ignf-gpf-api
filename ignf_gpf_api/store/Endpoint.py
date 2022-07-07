from typing import Dict, List, Optional, Type
from ignf_gpf_api.io.ApiRequester import ApiRequester

from ignf_gpf_api.store.StoreEntity import StoreEntity, T


class Endpoint(StoreEntity):
    """Classe Python représentant l'entité Endpoint (point de montage)."""

    _entity_name = "endpoint"
    _entity_title = "point de montage"

    @classmethod
    def api_list(cls: Type[T], infos_filter: Optional[Dict[str, str]] = None, tags_filter: Optional[Dict[str, str]] = None, page: Optional[int] = None) -> List[T]:
        """Liste les points de montage de l'API respectant les paramètres donnés.

        Args:
            infos_filter (Optional[Dict[str, str]]): dictionnaire contenant les paramètres de filtre sous la forme {"nom_info": "valeur_info"}
            tags_filter (Optional[Dict[str, str]]): dictionnaire contenant les tag de filtre sous la forme {"nom_tag": "valeur_tag"}
            page (Optional[int]): page à récupérer, toutes si None. Default to None.

        Returns:
            List[T]: liste des entités retournées
        """
        # Gestion des paramètres nuls
        infos_filter = infos_filter if infos_filter is not None else {}
        tags_filter = tags_filter if tags_filter is not None else {}

        # Requête
        o_response = ApiRequester().route_request("datastore_get")

        # Liste pour stocker les endpoints correspondants
        l_endpoints: List[T] = []

        # Pour chaque endpoints en dictionnaire
        for d_endpoint in o_response.json()["endpoints"]:
            # On suppose qu'il est ok
            b_ok = True
            # On vérifie s'il respecte les critère d'attributs
            for k, v in infos_filter.items():
                if d_endpoint["endpoint"].get(k) != v:
                    b_ok = False
                    break
            # S'il est ok au final, on l'ajoute
            if b_ok:
                l_endpoints.append(cls(d_endpoint["endpoint"]))
        # A la fin, on renvoie la liste
        return l_endpoints
