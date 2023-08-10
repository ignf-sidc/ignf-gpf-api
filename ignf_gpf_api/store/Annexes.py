from typing import List, Optional
import requests

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.PartialEditInterface import PartialEditInterface
from ignf_gpf_api.store.interface.ReUploadFileInterface import ReUploadFileInterface
from ignf_gpf_api.store.interface.DownloadInterface import DownloadInterface
from ignf_gpf_api.store.interface.CreatedByUploadFileInterface import CreatedByUploadFileInterface


class Annexes(CreatedByUploadFileInterface, DownloadInterface, PartialEditInterface, ReUploadFileInterface, StoreEntity):
    """Classe Python représentant l'entité Fichier statique (annexes).

    Cette classe permet d'effectuer les actions spécifiques liées aux fichiers statiques : création,
    remplacement, mise à jour, suppression.
    """

    _entity_name = "annexes"
    _entity_title = "annexes"

    @staticmethod
    def publish_by_label(labels: List[str], datastore: Optional[str] = None) -> int:
        """Publication de toutes les annexes ayant les labels indiqués.

        Args:
            labels (List[str]): liste des labels
            datastore (Optional[str], optional): Identifiant du datastore

        Returns:
            int: nombre d'annexes publiées
        """

        # Génération du nom de la route
        s_route = f"{Annexes._entity_name}_publish_by_label"

        # Requête
        o_response: requests.Response = ApiRequester().route_request(
            s_route,
            route_params={"datastore": datastore},
            params={"labels": labels},
            method=ApiRequester.POST,
        )

        return int(o_response.text)

    @staticmethod
    def unpublish_by_label(labels: List[str], datastore: Optional[str] = None) -> int:
        """dépublication de toutes les annexes portent l'ensemble de label

        Args:
            labels (List[str]): liste des labels
            datastore (Optional[str], optional): Identifiant du datastore

        Returns:
            int: nombre d'annexes de dépublier
        """

        # Génération du nom de la route
        s_route = f"{Annexes._entity_name}_unpublish_by_label"

        # Requête
        o_response: requests.Response = ApiRequester().route_request(
            s_route,
            route_params={"datastore": datastore},
            params={"labels": labels},
            method=ApiRequester.POST,
        )

        return int(o_response.text)
