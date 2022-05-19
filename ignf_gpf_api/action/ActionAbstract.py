from abc import ABC, abstractmethod
import json
from typing import Any, Dict, Optional

from ignf_gpf_api.action.Errors import StepActionError
from ignf_gpf_api.action.GlobalResolver import GlobalResolver
from ignf_gpf_api.io.Config import Config


class ActionAbstract(ABC):
    """Classe représentant une action d'un workflow.

    Attributes :
        __workflow_name (str) : nom du workflow
        __definition_dict (Dict[str, Any]) : définition de l'action
        __parent_action (Optional["Action"]) : action parente
    """

    def __init__(self, workflow_name: str, definition_dict: Dict[str, Any], parent_action: Optional["ActionAbstract"] = None) -> None:
        super().__init__()
        self.__workflow_name: str = workflow_name
        self.__definition_dict: Dict[str, Any] = definition_dict
        self.__parents_action: Optional["ActionAbstract"] = parent_action

    @property
    def workflow_name(self) -> str:
        return self.__workflow_name

    @property
    def definition_dict(self) -> Dict[str, Any]:
        return self.__definition_dict

    @property
    def parent_action(self) -> Optional["ActionAbstract"]:
        return self.__parents_action

    def resolve(self) -> None:
        """Résout la définition de l'action"""
        Config().om.info("Résolution de la configuration...")
        # Pour faciliter la résolution, on repasse la définition de l'action en json
        s_definition = str(json.dumps(self.__definition_dict))
        # lancement des résolveurs
        s_resolved_definition = GlobalResolver().resolve(s_definition)
        # on repasse en json
        self.__definition_dict = json.loads(s_resolved_definition)

    @abstractmethod
    def run(self) -> None:
        """lancement de l'exécution de l'action"""

    # désactivation des imports en haut de page => problème d'import circulaire
    # pylint:disable=import-outside-toplevel
    @staticmethod
    def generate(workflow_name: str, definition_dict: Dict[str, Any], parent_action: Optional["ActionAbstract"] = None) -> "ActionAbstract":
        """génération de la bonne action selon le type

        Args:
            workflow_name (str): non du workflow
            definition_dict (Dict[str, Any]): dictionnaire définissant l'action
            parent_action (Optional[&quot;ActionAbstract&quot;], optional): action précédente (si étape à plusieurs action). Defaults to None.

        Returns:
            ActionAbstract: instance permettant de lancer l'action
        """
        if definition_dict["type"] == "processing-execution":

            import ignf_gpf_api.action.ProcessingExecutionAction

            return ignf_gpf_api.action.ProcessingExecutionAction.ProcessingExecutionAction(workflow_name, definition_dict, parent_action)
        if definition_dict["type"] == "configuration":
            import ignf_gpf_api.action.ConfigurationAction

            return ignf_gpf_api.action.ConfigurationAction.ConfigurationAction(workflow_name, definition_dict, parent_action)
        if definition_dict["type"] == "offering":
            import ignf_gpf_api.action.OfferingAction

            return ignf_gpf_api.action.OfferingAction.OfferingAction(workflow_name, definition_dict, parent_action)
        raise StepActionError(f"Aucune correspondance pour ce type d'action : {definition_dict['type']}")
