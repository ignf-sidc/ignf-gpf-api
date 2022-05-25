from typing import Any, Dict, Optional
from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract


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
        # Création de la Configuration
        self.__create_configuration()
        # Ajout des tags sur l'Upload ou la StoredData
        self.__add_tags()
        # Ajout des commentaires sur l'Upload ou la StoredData
        self.__add_comments()

    def __create_configuration(self) -> None:
        """Création de la Configuration sur l'API à partir des paramètres de définition de l'action."""
        raise NotImplementedError("ConfigurationAction.__create_configuration")

    def __add_tags(self) -> None:
        """Ajout des tags sur la Configuration."""
        raise NotImplementedError("ConfigurationAction.__add_tags")

    def __add_comments(self) -> None:
        """Ajout des commentaires sur la Configuration."""
        raise NotImplementedError("ConfigurationAction.__add_comments")

    @property
    def configuration(self) -> Optional[Configuration]:
        return self.__configuration
