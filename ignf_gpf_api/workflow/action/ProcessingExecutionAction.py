from pyclbr import Function
from typing import Any, Dict, Optional
from ignf_gpf_api.store.ProcessingExecution import ProcessingExecution
from ignf_gpf_api.store.StoredData import StoredData
from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.store.Upload import Upload


class ProcessingExecutionAction(ActionAbstract):
    """classe dédiée à la création des ProcessingExecution.

    Attributes :
        __workflow_context (str) : nom du context du workflow
        __definition_dict (Dict[str, Any]) : définition de l'action
        __parent_action (Optional["Action"]) : action parente
        __processing_execution (Optional[ProcessingExecution]) : représentation Python de l'exécution de traitement créée
        __Upload (Optional[Upload]) : représentation Python de la livraison en sortie (null si données stockée en sortie)
        __StoredData (Optional[StoredData]) : représentation Python de la données stockée en sortie (null si livraison en sortie)
    """

    def __init__(self, workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional["ActionAbstract"] = None) -> None:
        super().__init__(workflow_context, definition_dict, parent_action)
        # Autres attributs
        self.__processing_execution: Optional[ProcessingExecution] = None
        self.__upload: Optional[Upload] = None
        self.__stored_data: Optional[StoredData] = None

    def run(self) -> None:
        # Création de l'exécution du traitement (attributs processing_execution et Upload/StoredData défini)
        self.__create_processing_execution()
        # Ajout des tags sur l'Upload ou la StoredData
        self.__add_tags()
        # Ajout des commentaires sur l'Upload ou la StoredData
        self.__add_comments()
        # Lancement du traitement
        self.__launch()

    def __create_processing_execution(self) -> None:
        """Création du ProcessingExecution sur l'API à partir des paramètres de définition de l'action.
        Récupération des attributs processing_execution et Upload/StoredData.
        """
        raise NotImplementedError("ProcessingExecutionAction.__create_processing_execution")

    def __add_tags(self) -> None:
        """Ajout des tags sur l'Upload ou la StoredData en sortie du ProcessingExecution."""
        raise NotImplementedError("ProcessingExecutionAction.__add_tags")

    def __add_comments(self) -> None:
        """Ajout des commentaires sur l'Upload ou la StoredData en sortie du ProcessingExecution."""
        raise NotImplementedError("ProcessingExecutionAction.__add_comments")

    def __launch(self) -> None:
        """Lancement de la ProcessingExecution."""
        raise NotImplementedError("ProcessingExecutionAction.__launch")

    def monitoring_until_end(self, callback: Optional[Function] = None) -> Optional[bool]:
        """Attend que la ProcessingExecution soit terminée (SUCCESS, FAILURE, ABORTED) avant de rendre la main.
        La fonction callback indiquée est exécutée en prenant en paramètre la différence de log entre deux vérifications.

        Args:
            callback (Optional[Function], optional): fonction de callback à exécuter avec la différence de log entre deux vérifications. Defaults to None.

        Returns:
            Optional[bool]: True si SUCCESS, False si FAILURE, None si ABORTED
        """
        raise NotImplementedError("ProcessingExecutionAction.monitoring_until_end")

    @property
    def processing_execution(self) -> Optional[ProcessingExecution]:
        return self.__processing_execution

    @property
    def upload(self) -> Optional[Upload]:
        return self.__upload

    @property
    def stored_data(self) -> Optional[StoredData]:
        return self.__stored_data
