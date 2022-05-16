from ignf_gpf_api.store.StoreEntity import StoreEntity


class ProcessingExecution(StoreEntity):
    """Classe Python représentant l'entité ProcessingExecution (exécution d'un traitement)."""

    _entity_name = "processing_execution"
    _entity_title = "exécution d'un traitement"

    def api_logs(self) -> str:
        """Récupère les logs de cette exécution de traitement sur l'API.

        Returns:
            str: les logs récupérés
        """
        raise NotImplementedError("ProcessingExecution.api_logs")

    def api_launch(self) -> None:
        """Lance l'exécution du traitement sur l'API."""
        raise NotImplementedError("ProcessingExecution.api_launch")

    def api_abort(self) -> None:
        """Annule l'exécution du traitement sur l'API."""
        raise NotImplementedError("ProcessingExecution.api_abort")
