from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.StoreEntity import StoreEntity


class CheckExecution(StoreEntity):
    """Classe Python représentant l'entité CheckExecution (exécution d'une vérification)."""

    _entity_name = "check_execution"
    _entity_title = "exécution d'une vérification"

    STATUS_WAITING = "WAITING"
    STATUS_PROGRESS = "PROGRESS"
    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAILURE = "FAILURE"

    def api_logs(self) -> str:
        """Récupère les logs de cette exécution de vérification sur l'API.

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
        return s_log
