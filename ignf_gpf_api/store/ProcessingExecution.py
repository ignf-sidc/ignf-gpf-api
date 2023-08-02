from datetime import datetime
import json
from typing import Optional

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.CsfInterface import CsfInterface
from ignf_gpf_api.io.ApiRequester import ApiRequester


class ProcessingExecution(CsfInterface, StoreEntity):
    """Classe Python représentant l'entité ProcessingExecution (exécution d'un traitement).

    Cette classe permet d'effectuer les actions spécifiques liées aux exécution de traitement : création,
    lancement, gestion de l'exécution, récupération du log, etc.
    """

    _entity_name = "processing_execution"
    _entity_title = "exécution d'un traitement"

    STATUS_CREATED = "CREATED"
    STATUS_WAITING = "WAITING"
    STATUS_PROGRESS = "PROGRESS"
    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAILURE = "FAILURE"
    STATUS_ABORTED = "ABORTED"

    def api_logs(self) -> str:
        """Récupère les logs de cette exécution de traitement sur l'API.

        Returns:
            str: les logs récupérés
        """
        # Génération du nom de la route
        s_route = f"{self._entity_name}_logs"
        # Requête "get"
        o_response = ApiRequester().route_request(
            s_route,
            route_params={self._entity_name: self.id, "datastore": self.datastore},
        )
        s_log = o_response.text
        try:
            if s_log in ["", "[]"]:
                return ""
            # les logs sont retourné sous forme de liste on tente le passage de liste à un texte propre.
            l_log = json.loads(s_log)
            s_log = "\n".join(l_log)
        except Exception:
            pass
        # on renvoie les logs
        return s_log

    def api_launch(self) -> None:
        """Lance l'exécution du traitement sur l'API."""
        # Génération du nom de la route
        s_route = f"{self._entity_name}_launch"

        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id, "datastore": self.datastore},
        )

    def api_abort(self) -> None:
        """Annule l'exécution du traitement sur l'API."""
        # Génération du nom de la route
        s_route = f"{self._entity_name}_abort"

        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id, "datastore": self.datastore},
        )

    @property
    def launch(self) -> Optional[datetime]:
        """Récupère la datetime de lancement de l'exécution du traitement.

        Returns:
            datetime: datetime de lancement de l'exécution du traitement
        """
        return self._get_datetime("launch")
