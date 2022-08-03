import json
from abc import ABC
from typing import Any, Dict, List, Optional, Type, TypeVar

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.Errors import StoreEntityError

T = TypeVar("T", bound="StoreEntity")


class StoreEntity(ABC):
    """StoreEntity : représentation Python d'une entité de l'entrepôt.

    Args:
        store_api_dict (Dict[str, Any]) : propriétés de l'entité dans la même forme que celle renvoyée par l'API

    Attributes:
        _store_api_dict (Dict[str, Any]) : propriétés de l'entité dans la même forme que celle renvoyée par l'API
    """

    # ATTRIBUTS DE CLASSE (* => Attribut à écraser par les classes filles)
    # (*) Nom "technique" de l'entité (pour compléter le nom des routes par exemple)
    _entity_name: str = "store_entity"
    # (*) Nom "utilisateur" de l'entité (pour afficher une message par exemple)
    _entity_title: str = "Entité Abstraite"

    def __init__(self, store_api_dict: Dict[str, Any]) -> None:
        self._store_api_dict: Dict[str, Any] = store_api_dict

    ##############################################################
    # Propriétés d'accès
    ##############################################################

    @property
    def id(self) -> str:
        """Renvoie l'identifiant du StoreEntity
        Returns:
            str: l'identifiant du StoreEntity
        """
        return str(self._store_api_dict["_id"])

    def get_store_properties(self) -> Dict[str, Any]:
        """Renvoie les propriétés de la StoreEntity
        Returns:
            Dict[str, Any]: propriétés de l'entité (sous la même forme que celle renvoyée par l'API)
        """
        return self._store_api_dict

    @classmethod
    def entity_name(cls) -> str:
        return cls._entity_name

    @classmethod
    def entity_title(cls) -> str:
        return cls._entity_title

    ##############################################################
    # Fonction d'interface avec l'API
    ##############################################################

    @classmethod
    def api_create(cls: Type[T], data: Optional[Dict[str, Any]], route_params: Optional[Dict[str, Any]] = None) -> T:
        """Crée une nouvelle entité dans l'API.

        Args:
            data (Optional[Dict[str, Any]]): Données nécessaires pour la création
            route_params (Optional[Dict[str, Any]]): paramètres de résolution de la route. Defaults to None.

        Returns:
            StoreEntity: entité créée
        """
        # Génération du nom de la route
        s_route = f"{cls._entity_name}_create"
        # Requête
        o_response = ApiRequester().route_request(
            s_route,
            route_params=route_params,
            method=ApiRequester.POST,
            data=data,
        )
        # Instanciation
        return cls(o_response.json())

    @classmethod
    def api_get(cls: Type[T], id_: str) -> T:
        """Récupère une entité depuis l'API.

        Args:
            id_ (var): identifiant de l'entité

        Returns:
            StoreEntity: l'entité instanciée correspondante
        """
        # Génération du nom de la route
        s_route = f"{cls._entity_name}_get"
        # Requête
        o_response = ApiRequester().route_request(
            s_route,
            route_params={cls._entity_name: id_},
        )
        # Instanciation
        return cls(o_response.json())

    @classmethod
    def api_list(cls: Type[T], infos_filter: Optional[Dict[str, str]] = None, tags_filter: Optional[Dict[str, str]] = None, page: Optional[int] = None) -> List[T]:
        """Liste les entités de l'API respectant les paramètres donnés.

        Args:
            infos_filter (Optional[Dict[str, str]]): dictionnaire contenant les paramètres de filtre sous la forme {"nom_info": "valeur_info"}
            tags_filter (Optional[Dict[str, str]]): dictionnaire contenant les tag de filtre sous la forme {"nom_tag": "valeur_tag"}
            page (Optional[int]): page à récupérer, toutes si None. Default to None.

        Returns:
            List[StoreEntity]: liste des entités retournées
        """
        # Nombre d'éléments max à lister par requête
        i_limit = Config().get_int("store_api", "nb_limit")

        # Gestion des paramètres nuls
        infos_filter = infos_filter if infos_filter is not None else {}
        tags_filter = tags_filter if tags_filter is not None else {}

        # Fusion des filtres sur les attributs et les tags
        d_params: Dict[str, Any] = infos_filter if infos_filter is not None else {}
        d_params["tags[]"] = [f"{k}={v}" for k, v in tags_filter.items()]

        # Génération du nom de la route
        s_route = f"{cls._entity_name}_list"

        # Liste pour stocker les entités
        l_entities: List[T] = []

        # Numéro de la page demandée
        i_page = 1 if page is None else page

        # Flag indiquant s'il faut requêter la prochaine page
        b_next_page = True

        # On requête tant qu'on est à la page spécifiquement demandée ou qu'on veut toutes les pages et que la dernière n'était pas vide
        while i_page == page or (page is None and b_next_page is True):
            # On liste les entités à la bonne page
            o_response = ApiRequester().route_request(
                s_route,
                params={**d_params, **{"page": i_page, "limit": i_limit}},
            )
            # On les ajoute à la liste
            l_entities += [cls(i) for i in o_response.json()]
            # On regarde le Content-Range de la réponse pour savoir si on doit refaire une requête pour récupérer la fin
            b_next_page = ApiRequester.range_next_page(o_response.headers.get("Content-Range"), len(l_entities))
            # On passe à la page suivante
            i_page += 1

        # On renvoie la liste des entités récupérées
        return l_entities

    def api_delete(self) -> None:
        """Supprime l'entité de l'API."""
        s_route = f"{self._entity_name}_delete"
        # Requête
        ApiRequester().route_request(s_route, method=ApiRequester.DELETE, route_params={self._entity_name: self.id})

    def api_update(self) -> None:
        """Met à jour l'instance Python représentant l'entité en récupérant les infos à jour sur l'API."""
        # Génération du nom de la route
        s_route = f"{self._entity_name}_get"
        # Requête
        o_response = ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id},
        )
        # Mise à jour du stockage local
        self._store_api_dict = o_response.json()

    @staticmethod
    def filter_dict_from_str(filters: Optional[str]) -> Dict[str, str]:
        """Les filtres de store_entities basés sur les tags ou les propriétés sont écrits sous la forme `name=value,name=value`.
        Cette fonction transforme une liste de tags sous cette forme en dictionnaire de la forme `{"name":"value","name":"value"}`.

        Args:
            filters (Optional[str]): Liste de filtres ayant la forme `name=value,name=value`

        Returns:
            Dict[str, str]: Dictionnaire ayant la forme `{"name": "value", "name": "value"}`

        Examples:
            Conversion classique :
            >>> filter_dict_from_str("name=value,name=value")
            {'name':'value','name':'value'}

            Les espaces ne changent rien :
            >>> filter_dict_from_str("name = value , name= value")
            {'name':'value','name':'value'}

            La valeur None renvoie un dictionnaire vide
            >>> filter_dict_from_str(None)
            {}

        Raises:
            StoreEntityError : si un filtre ne contient pas le caractère '='
        """
        # Dictionnaire résultat
        d_filter: Dict[str, str] = {}
        if filters is not None:
            # On extrait les filtres séparés par une virgule
            l_filter = filters.split(",")

            # Pour chaque filtre
            for s_filter in l_filter:
                # on extrait le nom du tag et sa valeur (séparés par un '=') après avoir enlevé d'éventuels espaces (devant ou derrière => trim)
                l_filter_infos = s_filter.split("=")
                if len(l_filter_infos) == 2:
                    d_filter[l_filter_infos[0].strip()] = l_filter_infos[1].strip()
                else:
                    s_error_message = f"filter_tags_dict_from_str : le filtre '{s_filter}' ne contient pas le caractère '='"
                    Config().om.error(s_error_message)
                    raise StoreEntityError(s_error_message)
        return d_filter

    ##############################################################
    # Récupération du JSON
    ##############################################################

    def to_json(self, indent: Optional[int] = None) -> str:
        """Renvoie les données JSON de l'entité éventuellement formatées.

        Args:
            indent (Optional[int], optional): Nombre d'espaces pour chaque indentation. Defaults to None.

        Returns:
            str: Donnée JSON
        """
        return json.dumps(self._store_api_dict, indent=indent)

    ##############################################################
    # Fonction d'accès général
    ##############################################################

    def __getitem__(self, key: str) -> Any:
        # La classe se comporte comme un dictionnaire
        # et permet de récupérer les info de _store_api_dict
        return self._store_api_dict[key]

    ##############################################################
    # Fonction test d'égalité
    ##############################################################

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, StoreEntity):
            return self.id == obj.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    ##############################################################
    # Fonctions de représentation
    ##############################################################
    def __str__(self) -> str:
        # Affichage à destination d'un utilisateur.
        # On affiche l'id et le nom si possible.

        # Liste pour stocker les infos à afficher
        l_infos = []
        # Ajout de l'id
        l_infos.append(f"id={self.id}")
        # Ajout du nom si possible
        if "name" in self._store_api_dict:
            l_infos.append(f"name={self['name']}")
        # Retour
        return f"{self.__class__.__name__}({', '.join(l_infos)})"

    def __repr__(self) -> str:
        # Affichage à destination d'un développeur.
        # Pour le moment, pas de différence avec __str__
        return str(self)
