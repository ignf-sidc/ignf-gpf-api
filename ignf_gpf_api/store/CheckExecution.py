from ignf_gpf_api.store.StoreEntity import StoreEntity


class CheckExecution(StoreEntity):
    """Classe Python représentant l'entité CheckExecution (exécution d'une vérification)."""

    _entity_name = "check_execution"
    _entity_title = "exécution d'une vérification"

    def api_logs(self) -> str:
        """Récupère les logs de cette exécution de vérification sur l'API.

        Returns:
            str: les logs récupérés
        """
        raise NotImplementedError("CheckExecution.api_logs")
