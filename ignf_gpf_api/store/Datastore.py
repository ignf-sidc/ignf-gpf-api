from typing import Dict, List, Optional, Type, TypeVar

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.StoreEntity import StoreEntity

T = TypeVar("T", bound="StoreEntity")


class Datastore(StoreEntity):
    """Classe Python représentant l'entité Store (entrepôt)."""

    _entity_name = "datastore"
    _entity_title = "entrepôt"

    @classmethod
    def api_list(cls: Type[T], infos_filter: Optional[Dict[str, str]] = None, tags_filter: Optional[Dict[str, str]] = None, page: Optional[int] = None) -> List[T]:
        """Liste les entités de l'API respectant les paramètres donnés.

        Args:
            infos_filter: Filtres sur les attributs sous la forme `{"nom_attribut": "valeur_attribut"}`
            tags_filter: Filtres sur les tags sous la forme `{"nom_tag": "valeur_tag"}`
            page: Numéro page à récupérer, toutes si None.

        Returns:
            (List[StoreEntity]): liste des entités retournées par l'API
        """
        # Gestion des paramètres nuls
        infos_filter = infos_filter if infos_filter is not None else {}

        # Fusion des filtres sur les attributs et les tags
        s_filter_name = infos_filter.get("name")

        # Liste pour stocker les entités
        l_entities: List[T] = []

        # On liste les communautés de l'utilisateur
        o_response = ApiRequester().route_request("user_get")
        # Pour chacune d'elles
        for d_communities_member in o_response.json()["communities_member"]:
            # On récupère le nom et le nom technique
            s_name = d_communities_member["community"]["name"]
            s_technical_name = d_communities_member["community"]["technical_name"]
            # S'il y a pas de filtre ou que celui-ci correspond
            if s_filter_name is None or (s_filter_name in (s_name, s_technical_name)):
                # On ajoute le datastore à la liste
                l_entities.append(
                    cls(
                        {
                            "_id": d_communities_member["community"]["datastore"],
                            "name": s_name,
                            "technical_name": s_technical_name,
                        }
                    )
                )

        # On renvoie la liste des entités récupérées
        return l_entities
