import time
from typing import Any, Callable, Dict, Optional

from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.ProcessingExecution import ProcessingExecution
from ignf_gpf_api.store.StoredData import StoredData
from ignf_gpf_api.workflow.Errors import StepActionError
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
        # création de la ProcessingExecution
        self.__processing_execution = ProcessingExecution.api_create(self.definition_dict["parameters"])

        d_info = self.__processing_execution.get_store_properties()["output"]
        if "upload" in d_info:
            # récupération de l'upload
            self.__upload = Upload.api_get(d_info["upload"]["_id"])
        elif "stored_data" in d_info:
            # récupération de la stored_data
            self.__stored_data = StoredData.api_get(d_info["stored_data"]["_id"])
        else:
            raise StepActionError(f"Aucune correspondance pour {d_info.keys()}")

    def __add_tags(self) -> None:
        """Ajout des tags sur l'Upload ou la StoredData en sortie du ProcessingExecution."""
        if "tags" not in self.definition_dict or self.definition_dict["tags"] == {}:
            # cas on a pas de tag ou vide: on ne fait rien
            return
        # on ajoute le tag
        if self.__upload is not None:
            self.__upload.api_add_tags(self.definition_dict["tags"])
        elif self.__stored_data is not None:
            self.__stored_data.api_add_tags(self.definition_dict["tags"])
        else:
            # on a pas de stored_data ni de upload
            raise StepActionError("aucune upload ou stored-data trouvé. Impossible d'ajouter les tags")

    def __add_comments(self) -> None:
        """Ajout des commentaires sur l'Upload ou la StoredData en sortie du ProcessingExecution."""
        if "comments" not in self.definition_dict:
            # cas on a pas de commentaires : on ne fait rien
            return
        # on ajoute le commentaires
        if self.__upload is not None:
            for s_comment in self.definition_dict["comments"]:
                self.__upload.api_add_comment({"text": s_comment})
        elif self.__stored_data is not None:
            for s_comment in self.definition_dict["comments"]:
                self.__stored_data.api_add_comment({"text": s_comment})
        else:
            # on a pas de stored_data ni de upload
            raise StepActionError("aucune upload ou stored-data trouvé. Impossible d'ajouter les commentaires")

    def __launch(self) -> None:
        """Lancement de la ProcessingExecution."""
        if self.__processing_execution is not None:
            self.__processing_execution.api_launch()
        else:
            raise StepActionError("aucune procession-execution de trouvé. Impossible de lancer le traitement")

    def monitoring_until_end(self, callback: Optional[Callable[[ProcessingExecution], None]] = None) -> str:
        """Attend que la ProcessingExecution soit terminée (SUCCESS, FAILURE, ABORTED) avant de rendre la main.
        La fonction callback indiquée est exécutée en prenant en paramètre le log du traitement et le status du traitement (callback(logs, status)).

        Args:
            callback (Optional[Callable[[ProcessingExecution], None]], optional): fonction de callback à exécuter prend en argument le traitement (callback(processing-execution)). Defaults to None.

        Returns:
            Optional[bool]: True si SUCCESS, False si FAILURE, None si ABORTED
        """
        # NOTE :  Ne pas utiliser self.__processing_execution mais self.processing_execution pour facilité les testes
        i_nb_sec_between_check = Config().get_int("processing_execution", "nb_sec_between_check_updates")
        Config().om.info(f"Monitoring du traitement toutes les {i_nb_sec_between_check} secondes...")
        if self.processing_execution is None:
            raise StepActionError("Aucune procession-execution de trouvé. Impossible de suivre le déroulement du traitement")
        s_status = self.processing_execution.get_store_properties()["status"]
        while s_status not in [ProcessingExecution.STATUS_ABORTED, ProcessingExecution.STATUS_SUCCESS, ProcessingExecution.STATUS_FAILURE]:
            # appel de la fonction affichant les logs
            if callback is not None:
                callback(self.processing_execution)
            # On attend le temps demandé
            time.sleep(i_nb_sec_between_check)
            # On met à jour __processing_execution
            self.processing_execution.api_update()
            s_status = self.processing_execution.get_store_properties()["status"]
        # Si on est sorti c'est que c'est fini
        ## dernier affichage
        if callback is not None:
            callback(self.processing_execution)
        ## on return le status de fin
        return str(s_status)

    @property
    def processing_execution(self) -> Optional[ProcessingExecution]:
        return self.__processing_execution

    @property
    def upload(self) -> Optional[Upload]:
        return self.__upload

    @property
    def stored_data(self) -> Optional[StoredData]:
        return self.__stored_data
