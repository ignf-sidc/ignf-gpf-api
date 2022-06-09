from typing import Any, Callable, Dict, Optional

from ignf_gpf_api.store.ProcessingExecution import ProcessingExecution
from ignf_gpf_api.workflow.Errors import WorkflowError
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.workflow.action.ProcessingExecutionAction import ProcessingExecutionAction
from ignf_gpf_api.workflow.action.ConfigurationAction import ConfigurationAction
from ignf_gpf_api.workflow.action.OfferingAction import OfferingAction


class Workflow:
    """Description et lancement d'un workflow
    Attributes :
        __name (string) : nom du workflow
        __raw_definition_dict (dict) : définition du workflow
    """

    def __init__(self, name: str, raw_dict: Dict[str, Any]) -> None:
        """Constructeur

        Args:
            name (string) : nom du workflow
            raw_dict (dict): workflow non résolu
        """
        self.__name = name
        self.__raw_definition_dict = raw_dict

    def get_raw_dict(self) -> Dict[str, Any]:
        """Renvoie le dictionnaire de définition du workflow
        Returns :
            dict : le dictionnaire de définition du workflow
        """
        return self.__raw_definition_dict

    def run_step(self, step_name: str, callback: Optional[Callable[[ProcessingExecution], None]] = None) -> None:
        """Lance une étape du workflow à partir de son nom
        Args:
            step_name (string): nom de l'étape
        Raises:
            WorkflowExecutionError: est levée si un problème apparaît pendant l'exécution du workflow
        """
        Config().om.info(f"Lancement de l'étape {step_name}")
        # Récupération de l'étape dans la définition de workflow
        d_step_definition = self.__get_step_definition(step_name)
        # initialisation des actions parentes
        l_parentes = None
        # Pour chaque action définie dans le workflow, instanciation de l'objet Action puis création sur l'entrepôt
        for d_action_raw in d_step_definition["actions"]:
            # création de l'action
            o_action = Workflow.generate(f"{step_name}/{d_action_raw['type']}", d_action_raw, l_parentes)
            # résolution
            o_action.resolve()
            # exécution de l'action :
            o_action.run()
            # on attend la fin de l'exécution si besoin
            if isinstance(o_action, ProcessingExecutionAction):
                s_status = o_action.monitoring_until_end(callback=callback)
                if s_status != ProcessingExecution.STATUS_SUCCESS:
                    s_error_message = f"Le ProcessingExecution {o_action} ne s'est pas bien passé. Sortie {s_status}"
                    Config().om.error(s_error_message)
                    raise WorkflowError(s_error_message)
            # cette action sera la parente de la suivante
            l_parentes = o_action

    def __get_step_definition(self, step_name: str) -> Dict[str, Any]:
        """Renvoie le dictionnaire correspondant à une étape du workflow à partir de son nom
        Args:
            step_name (string): nom de l'étape
        Raises:
            WorkflowExecutionError: est levée si l'étape n'existe pas dans le workflow
        """
        # Recherche de l'étape correspondante
        for o_step in self.__raw_definition_dict["workflow"]["steps"]:
            if o_step["name"] == step_name:
                return dict(o_step)

        # Si on passe la boucle, c'est que l'étape n'existe pas dans la définition du workflow
        s_error_message = f"L'étape {step_name} n'est pas définie dans le workflow {self.__name}"
        Config().om.error(s_error_message)
        raise WorkflowError(s_error_message)

    @staticmethod
    def generate(workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional[ActionAbstract] = None) -> ActionAbstract:
        """génération de la bonne action selon le type

        Args:
            workflow_context (str): nom du context du workflow
            definition_dict (Dict[str, Any]): dictionnaire définissant l'action
            parent_action (Optional[&quot;ActionAbstract&quot;], optional): action précédente (si étape à plusieurs action). Defaults to None.

        Returns:
            ActionAbstract: instance permettant de lancer l'action
        """
        if definition_dict["type"] == "processing-execution":
            return ProcessingExecutionAction(workflow_context, definition_dict, parent_action)
        if definition_dict["type"] == "configuration":
            return ConfigurationAction(workflow_context, definition_dict, parent_action)
        if definition_dict["type"] == "offering":
            return OfferingAction(workflow_context, definition_dict, parent_action)
        raise WorkflowError(f"Aucune correspondance pour ce type d'action : {definition_dict['type']}")
