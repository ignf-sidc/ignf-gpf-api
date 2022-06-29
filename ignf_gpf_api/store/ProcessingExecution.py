from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.io.ApiRequester import ApiRequester


class ProcessingExecution(StoreEntity):
    """Classe Python représentant l'entité ProcessingExecution (exécution d'un traitement)."""

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
            route_params={self._entity_name: self.id},
        )
        s_log = o_response.text
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
            route_params={self._entity_name: self.id},
        )

    def api_abort(self) -> None:
        """Annule l'exécution du traitement sur l'API."""
        # Génération du nom de la route
        s_route = f"{self._entity_name}_abort"

        # Requête
        ApiRequester().route_request(
            s_route,
            method=ApiRequester.POST,
            route_params={self._entity_name: self.id},
        )
