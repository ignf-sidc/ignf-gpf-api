from typing import Dict, List, Optional
from ignf_gpf_api.io.ApiRequester import ApiRequester

from ignf_gpf_api.store.StoreEntity import StoreEntity


class Endpoint(StoreEntity):
    """Classe Python représentant l'entité Endpoint (point de montage)."""

    _entity_name = "endpoint"
    _entity_title = "point de montage"

    @staticmethod
    def api_list(infos_filter: Optional[Dict[str, str]] = None, tags_filter: Optional[Dict[str, str]] = None) -> List["Endpoint"]:
        """Liste les points de montage de l'API respectant les paramètres donnés.

        Args:
            infos_filter (Optional[Dict[str, str]]): dictionnaire contenant les paramètres de filtre sous la forme {"nom_info": "valeur_info"}
            tags_filter (Optional[Dict[str, str]]): dictionnaire contenant les tag de filtre sous la forme {"nom_tag": "valeur_tag"}

        Returns:
            List[Endpoint]: liste des entités retournées
        """
        # Gestion des paramètres nuls
        infos_filter = infos_filter if infos_filter is not None else {}
        tags_filter = tags_filter if tags_filter is not None else {}

        # Requête
        o_response = ApiRequester().route_request("datastore_get")

        # Liste pour stocker les endpoints correspondants
        l_endpoints: List[Endpoint] = []

        # Pour chaque endpoints en dictionnaire
        for d_endpoint in o_response.json()["endpoints"]:
            # On suppose qu'il est ok
            b_ok = True
            # On vérifie s'il respecte les critère d'attributs
            for k, v in infos_filter.items():
                if d_endpoint.get(k) != v:
                    b_ok = False
                    break
            # S'il est ok au final, on l'ajoute
            if b_ok:
                l_endpoints.append(Endpoint(d_endpoint))
        # A la fin, on renvoie la liste
        return l_endpoints
