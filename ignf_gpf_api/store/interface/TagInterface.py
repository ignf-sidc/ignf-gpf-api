from typing import Dict, List
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.Errors import StoreEntityError
from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.io.ApiRequester import ApiRequester


class TagInterface(StoreEntity):
    """Interface de StoreEntity pour gérer les étiquettes (tags)."""

    def get_tag(self, tag_name: str) -> str:
        """Récupère la valeur d'un tag à partir de son nom
        Args:
            tag_name (str): nom du tag souhaité
        Raises :
            StoreEntityError : si le tag n'existe pas
        """
        # On vérifie que l'entité a bien une propriété tags et le tag souhaité
        if "tags" in self._store_api_dict and tag_name in self._store_api_dict["tags"]:
            return str(self._store_api_dict["tags"][tag_name])

        # Cas où l'entité ne possède pas ce nom de tag (ou pas de tag du tout)
        s_error_message = f"L'entité {self.__class__.__name__} {self.id} ne possède pas de tag {tag_name}"
        Config().om.error(s_error_message)
        raise StoreEntityError(s_error_message)

    def api_add_tags(self, tags_data: Dict[str, str]) -> None:
        """Ajout des tags à l'entité dans l'API.

        Args:
            tags_data (Dict[str, str]): liste des clés/valeurs à ajouter
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_add_tags"
        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id},
            data=tags_data,
        )

    def api_remove_tags(self, tag_keys: List[str]) -> None:
        """Supprime des tags de l'entité.

        Args:
            tag_keys (List[str]): liste des clés des tags à supprimer
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_delete_tags"
        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.DELETE,
            route_params={self._entity_name: self.id},
            # dans les paramètres (params), on met en clé "tag[]" et en valeur la liste des tags :
            params={"tags[]": tag_keys},
        )
