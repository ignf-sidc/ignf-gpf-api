import time
from typing import Any, Callable, Dict, Optional
from ignf_gpf_api.Errors import GpfApiError

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

    BEHAVIOR_STOP = "STOP"
    BEHAVIOR_DELETE = "DELETE"
    BEHAVIOR_CONTINUE = "CONTINUE"

    def __init__(self, workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional["ActionAbstract"] = None, behavior: Optional[str] = None) -> None:
        super().__init__(workflow_context, definition_dict, parent_action)
        # Autres attributs
        self.__processing_execution: Optional[ProcessingExecution] = None
        self.__upload: Optional[Upload] = None
        self.__stored_data: Optional[StoredData] = None
        self.__behavior: str = behavior if behavior is not None else Config().get("processing_execution", "behavior_if_exists")

    def run(self) -> None:
        Config().om.info("Création d'une exécution de traitement et complétion de l'entité en sortie...")
        # Création de l'exécution du traitement (attributs processing_execution et Upload/StoredData défini)
        self.__create_processing_execution()
        # Ajout des tags sur l'Upload ou la StoredData
        self.__add_tags()
        # Ajout des commentaires sur l'Upload ou la StoredData
        self.__add_comments()
        # Lancement du traitement
        self.__launch()
        # Affichage
        o_output_entity = self.__stored_data if self.__stored_data is not None else self.__upload
        Config().om.info(f"Exécution de traitement créée et lancée ({self.processing_execution}) et entité en sortie complétée ({o_output_entity}).")
        Config().om.info("Création d'une exécution de traitement et complétion de l'entité en sortie : terminé")

    def __create_processing_execution(self) -> None:
        """Création du ProcessingExecution sur l'API à partir des paramètres de définition de l'action.
        Récupération des attributs processing_execution et Upload/StoredData.
        """
        d_info: Optional[Dict[str, Any]] = None

        # On regarde si cette Exécution de Traitement implique la création d'une nouvelle entité (Livraison / Donnée Stockée)
        if self.output_new_entity:
            # TODO : gérer également les Livraison
            # On vérifie si une  Donnée Stockée équivalente à celle du dictionnaire de définition existe déjà
            o_stored_data = self.__find_stored_data()
            # Si on en a trouvée
            if o_stored_data is not None:
                # Comportement d'arrêt du programme
                if self.__behavior == self.BEHAVIOR_STOP:
                    raise GpfApiError(f"Impossible de créer l’exécution de traitement, une donnée stockée en sortie équivalente {o_stored_data} existe déjà.")
                # Comportement de suppression des entités détectées
                if self.__behavior == self.BEHAVIOR_DELETE:
                    Config().om.warning(f"Une donnée stockée équivalente à {o_stored_data} va être supprimée puis recréée.")
                    Config().om.warning("Si une exécution de traitement liée à la donnée équivalente existe, elle sera supprimée.")
                    # Récupération des traitements qui ont créé la donnée stockée équivalente
                    l_process = ProcessingExecution.api_list(infos_filter={"output_stored_data": o_stored_data.id})
                    for o_process in l_process:
                        # Suppression du traitement
                        o_process.api_delete()
                    # Suppression de la donnée stockée
                    o_stored_data.api_delete()
                    # création de la ProcessingExecution
                    self.__processing_execution = ProcessingExecution.api_create(self.definition_dict["body_parameters"])
                    d_info = self.__processing_execution.get_store_properties()["output"]
                # Comportements non supportés
                else:
                    raise GpfApiError(f"Le comportement {self.__behavior} n'est pas reconnu, l'exécution de traitement est annulée.")

        # A ce niveau là, si on a encore self.__processing_execution qui est None, c'est qu'on peut créer l'Exécution de Traitement sans problème
        if self.__processing_execution is None:
            # création de la ProcessingExecution
            self.__processing_execution = ProcessingExecution.api_create(self.definition_dict["body_parameters"])
            d_info = self.__processing_execution.get_store_properties()["output"]

        if d_info is None:
            Config().om.debug(self.__processing_execution.to_json(indent=4))
            raise GpfApiError("Erreur à la création de l'exécution de traitement : impossible de récupérer l'entité en sortie.")

        # Récupération des entités de l'exécution de traitement
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
        # on ajoute les tags
        if self.upload is not None:
            Config().om.info(f"Livraison {self.upload['name']} : ajout des {len(self.definition_dict['tags'])} tags...")
            self.upload.api_add_tags(self.definition_dict["tags"])
            Config().om.info(f"Livraison {self.upload['name']} : les {len(self.definition_dict['tags'])} tags ont été ajoutés avec succès.")
        elif self.stored_data is not None:
            Config().om.info(f"Donnée stockée {self.stored_data['name']} : ajout des {len(self.definition_dict['tags'])} tags...")
            self.stored_data.api_add_tags(self.definition_dict["tags"])
            Config().om.info(f"Donnée stockée {self.stored_data['name']} : les {len(self.definition_dict['tags'])} tags ont été ajoutés avec succès.")
        else:
            # on a pas de stored_data ni de upload
            raise StepActionError("aucune upload ou stored-data trouvé. Impossible d'ajouter les tags")

    def __add_comments(self) -> None:
        """Ajout des commentaires sur l'Upload ou la StoredData en sortie du ProcessingExecution."""
        if "comments" not in self.definition_dict:
            # cas on a pas de commentaires : on ne fait rien
            return
        # on ajoute les commentaires
        if self.upload is not None:
            Config().om.info(f"Livraison {self.upload['name']} : ajout des {len(self.definition_dict['comments'])} commentaires...")
            for s_comment in self.definition_dict["comments"]:
                self.upload.api_add_comment({"text": s_comment})
            Config().om.info(f"Livraison {self.upload['name']} : les {len(self.definition_dict['comments'])} commentaires ont été ajoutés avec succès.")
        elif self.stored_data is not None:
            Config().om.info(f"Donnée stockée {self.stored_data['name']} : ajout des {len(self.definition_dict['comments'])} commentaires...")
            for s_comment in self.definition_dict["comments"]:
                self.stored_data.api_add_comment({"text": s_comment})
            Config().om.info(f"Donnée stockée {self.stored_data['name']} : les {len(self.definition_dict['comments'])} commentaires ont été ajoutés avec succès.")
        else:
            # on a pas de stored_data ni de upload
            raise StepActionError("aucune upload ou stored-data trouvé. Impossible d'ajouter les commentaires")

    def __launch(self) -> None:
        """Lancement de la ProcessingExecution."""
        if self.processing_execution is not None:
            Config().om.info(f"Exécution de traitement {self.processing_execution['processing']['name']} : lancement...")
            self.processing_execution.api_launch()
            Config().om.info(f"Exécution de traitement {self.processing_execution['processing']['name']} : lancée avec succès.")

        else:
            raise StepActionError("aucune procession-execution de trouvé. Impossible de lancer le traitement")

    def __find_stored_data(self) -> Optional[StoredData]:
        """
        Fonction permettant de récupérer une stored Data en fonction des filtres définis dans default.ini

        Returns:
            Optional[StoredData]: données stockées retrouvée
        """
        # On tente de récupérer la stored_data selon les critères d'informations (nom...)
        l_attributes = Config().get("processing_execution", "uniqueness_constraint_infos").split(";")
        d_infos = {}
        d_dico = self.definition_dict["body_parameters"]["output"]
        for s_infos in l_attributes:
            if s_infos != "":
                if "stored_data" in d_dico:
                    d_infos[s_infos] = d_dico["stored_data"][s_infos]
        # On tente de récupérer la stored_data selon les critères de tags donnés en conf (uniqueness_constraint_tags)
        l_tags = Config().get("processing_execution", "uniqueness_constraint_tags").split(";")
        d_tags = {}
        for s_tag in l_tags:
            if s_tag != "":
                d_tags[s_tag] = self.definition_dict["tags"][s_tag]
        # On peut maintenant filtrer les stored data selon ces critères
        l_stored_data = StoredData.api_list(infos_filter=d_infos, tags_filter=d_tags)
        # S'il y a un ou plusieurs stored data, on retourne le 1er :
        if l_stored_data:
            return l_stored_data[0]
        # sinon on retourne None
        return None

    def monitoring_until_end(self, callback: Optional[Callable[[ProcessingExecution], None]] = None) -> str:
        """Attend que la ProcessingExecution soit terminée (SUCCESS, FAILURE, ABORTED) avant de rendre la main.
        La fonction callback indiquée est exécutée en prenant en paramètre le log du traitement et le status du traitement (callback(logs, status)).
        Si l'utilisateur stoppe le programme, la ProcessingExecution est arrêtée avant de quitter.

        Args:
            callback (Optional[Callable[[ProcessingExecution], None]], optional): fonction de callback à exécuter prend en argument le traitement (callback(processing-execution)). Defaults to None.

        Returns:
            Optional[bool]: True si SUCCESS, False si FAILURE, None si ABORTED
        """
        # NOTE :  Ne pas utiliser self.__processing_execution mais self.processing_execution pour faciliter les tests
        i_nb_sec_between_check = Config().get_int("processing_execution", "nb_sec_between_check_updates")
        Config().om.info(f"Monitoring du traitement toutes les {i_nb_sec_between_check} secondes...")
        if self.processing_execution is None:
            raise StepActionError("Aucune procession-execution de trouvé. Impossible de suivre le déroulement du traitement")
        try:
            s_status = self.processing_execution.get_store_properties()["status"]
            while s_status not in [ProcessingExecution.STATUS_ABORTED, ProcessingExecution.STATUS_SUCCESS, ProcessingExecution.STATUS_FAILURE]:
                # appel de la fonction affichant les logs
                if callback is not None:
                    callback(self.processing_execution)
                # On attend le temps demandé
                time.sleep(i_nb_sec_between_check)
                # On met à jour __processing_execution + valeur status
                self.processing_execution.api_update()
                s_status = self.processing_execution.get_store_properties()["status"]
            # Si on est sorti c'est que c'est fini
            ## dernier affichage
            if callback is not None:
                callback(self.processing_execution)
            ## on return le status de fin
            return str(s_status)
        except KeyboardInterrupt as e:
            # si le traitement est déjà dans un statu fini on ne fait rien => transmission de l'interruption
            self.processing_execution.api_update()
            s_status = self.processing_execution.get_store_properties()["status"]
            if s_status in [ProcessingExecution.STATUS_ABORTED, ProcessingExecution.STATUS_SUCCESS, ProcessingExecution.STATUS_FAILURE]:

                Config().om.warning("traitement déjà fini")
                raise
            # arrêt du traitement
            Config().om.warning("Ctrl+C : traitement en cours d’interruption, veuillez attendre...")
            self.processing_execution.api_abort()
            # attente que le traitement passe dans un statu fini
            self.processing_execution.api_update()
            s_status = self.processing_execution.get_store_properties()["status"]
            while s_status not in [ProcessingExecution.STATUS_ABORTED, ProcessingExecution.STATUS_SUCCESS, ProcessingExecution.STATUS_FAILURE]:
                # On attend 2s
                time.sleep(2)
                # On met à jour __processing_execution + valeur status
                self.processing_execution.api_update()
                s_status = self.processing_execution.get_store_properties()["status"]
            ## dernier affichage
            if callback is not None:
                callback(self.processing_execution)
            if s_status == ProcessingExecution.STATUS_ABORTED and self.output_new_entity:
                # suppression de l'upload ou la stored data en sortie
                if self.upload is not None:
                    Config().om.warning("Suppression de l'upload en cours de remplissage suite à l’interruption du programme")
                    self.upload.api_delete()
                elif self.stored_data is not None:
                    Config().om.warning("Suppression de la stored-data en cours de remplissage suite à l'interruption du programme")
                    self.stored_data.api_delete()
                # transmission de l'interruption
            raise KeyboardInterrupt() from e

    @property
    def processing_execution(self) -> Optional[ProcessingExecution]:
        return self.__processing_execution

    @property
    def upload(self) -> Optional[Upload]:
        return self.__upload

    @property
    def stored_data(self) -> Optional[StoredData]:
        return self.__stored_data

    @property
    def output_new_entity(self) -> bool:
        """Indique s'il y a création d'une nouvelle entité (clé "name" et non "_id" présente dans le paramètre "output" du corps de requête)."""
        d_output = self.definition_dict["body_parameters"]["output"]
        if "upload" in d_output:
            d_el = self.definition_dict["body_parameters"]["output"]["upload"]
        elif "stored_data" in d_output:
            d_el = self.definition_dict["body_parameters"]["output"]["stored_data"]
        else:
            return False
        return "name" in d_el
