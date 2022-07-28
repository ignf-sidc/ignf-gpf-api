from typing import Any, Dict, Optional
from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.io.Errors import ConflictError


class ConfigurationAction(ActionAbstract):
    """Classe dédiée à la création des Configuration.

    Attributes :
        __workflow_context (str) : nom du context du workflow
        __definition_dict (Dict[str, Any]) : définition de l'action
        __parent_action (Optional["Action"]) : action parente
        __configuration (Optional[Configuration]) : représentation Python de la configuration créée
    """

    def __init__(self, workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional["ActionAbstract"] = None) -> None:
        super().__init__(workflow_context, definition_dict, parent_action)
        # Autres attributs
        self.__configuration: Optional[Configuration] = None

    def run(self) -> None:
        Config().om.info("Création et complétion d'une configuration...")
        # Création de la Configuration
        self.__create_configuration()
        # Ajout des tags sur la Configuration
        self.__add_tags()
        # Ajout des commentaires sur la Configuration
        self.__add_comments()
        # Affichage
        Config().om.info(f"Configuration créée et complétée : {self.__configuration}")
        Config().om.info("Création et complétion d'une configuration : terminé")

    def __create_configuration(self) -> None:
        """Création de la Configuration sur l'API à partir des paramètres de définition de l'action."""
        # on gère une erreur de type ConflictError
        try:
            Config().om.info("Création de la configuration...")
            self.__configuration = Configuration.api_create(self.definition_dict["body_parameters"])
            Config().om.info(f"Configuration {self.__configuration['name']} créée avec succès.")
        except ConflictError:
            Config().om.warning("La configuration que vous tentez de créer existe déjà !")

    def __add_tags(self) -> None:
        """Ajout des tags sur la Configuration."""
        # on vérifie que la configuration et definition_dict ne sont pas null et on vérifie qu'il y'a bien une clé tags
        if self.configuration and self.definition_dict and "tags" in self.definition_dict and self.definition_dict["tags"] != {}:
            Config().om.info(f"Configuration {self.configuration['name']} : ajout des {len(self.definition_dict['tags'])} tags...")
            self.configuration.api_add_tags(self.definition_dict["tags"])
            Config().om.info(f"Configuration {self.configuration['name']} : les {len(self.definition_dict['tags'])} tags ont été ajoutés avec succès.")

    def __add_comments(self) -> None:
        """Ajout des commentaires sur la Configuration."""
        # on vérifie que la configuration et definition_dict ne sont pas null et on vérifie qu'il y'a bien une clé comments
        if self.configuration and self.definition_dict and "comments" in self.definition_dict and self.definition_dict["comments"] != {}:
            Config().om.info(f"Configuration {self.configuration['name']} : ajout des {len(self.definition_dict['comments'])} commentaires...")
            for s_comment in self.definition_dict["comments"]:
                self.configuration.api_add_comment({"text": s_comment})
            Config().om.info(f"Configuration {self.configuration['name']} : les {len(self.definition_dict['comments'])} commentaires ont été ajoutés avec succès.")

    @property
    def configuration(self) -> Optional[Configuration]:
        return self.__configuration
