from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import jsonschema  # type: ignore
from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.helper.JsonHelper import JsonHelper

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

    def run_step(self, step_name: str, callback: Optional[Callable[[ProcessingExecution], None]] = None, behavior: Optional[str] = None) -> None:
        """Lance une étape du workflow à partir de son nom

        Args:
            step_name (str): nom de l'étape
            callback (Optional[Callable[[ProcessingExecution], None]], optional): callback de suivi. Defaults to None.
            behavior (Optional[str]): comportement à adopter si une entité existe déjà sur l'entrepôt. Defaults to None.

        Raises:
            WorkflowError: levée si un problème apparaît pendant l'exécution du workflow
        """
        Config().om.info(f"Lancement de l'étape {step_name}...")
        # Récupération de l'étape dans la définition de workflow
        d_step_definition = self.__get_step_definition(step_name)
        # initialisation des actions parentes
        o_parent_action: Optional[ActionAbstract] = None
        # Pour chaque action définie dans le workflow, instanciation de l'objet Action puis création sur l'entrepôt
        for d_action_raw in d_step_definition["actions"]:
            # création de l'action
            o_action = Workflow.generate(f"{step_name}", d_action_raw, o_parent_action, behavior)
            # résolution
            o_action.resolve()
            # exécution de l'action
            Config().om.info(f"Exécution de l'action '{o_action.workflow_context}-{o_action.index}'...")
            o_action.run()
            # on attend la fin de l'exécution si besoin
            if isinstance(o_action, ProcessingExecutionAction):
                s_status = o_action.monitoring_until_end(callback=callback)
                if s_status != ProcessingExecution.STATUS_SUCCESS:
                    s_error_message = f"Le ProcessingExecution {o_action} ne s'est pas bien passé. Sortie {s_status}"
                    Config().om.error(s_error_message)
                    raise WorkflowError(s_error_message)
            Config().om.info(f"Exécution de l'action '{o_action.workflow_context}-{o_action.index}' : terminée")
            # cette action sera la parente de la suivante
            o_parent_action = o_action

    def __get_step_definition(self, step_name: str) -> Dict[str, Any]:
        """Renvoie le dictionnaire correspondant à une étape du workflow à partir de son nom.
        Lève une WorkflowError avec un message clair si l'étape n'est pas trouvée.
        Args:
            step_name (string): nom de l'étape
        Raises:
            WorkflowExecutionError: est levée si l'étape n'existe pas dans le workflow
        """
        # Recherche de l'étape correspondante
        if step_name in self.__raw_definition_dict["workflow"]["steps"]:
            return dict(self.__raw_definition_dict["workflow"]["steps"][step_name])

        # Si on passe le if, c'est que l'étape n'existe pas dans la définition du workflow
        s_error_message = f"L'étape {step_name} n'est pas définie dans le workflow {self.__name}"
        Config().om.error(s_error_message)
        raise WorkflowError(s_error_message)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def steps(self) -> List[str]:
        return list(self.__raw_definition_dict["workflow"]["steps"].keys())

    @staticmethod
    def generate(workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional[ActionAbstract] = None, behavior: Optional[str] = None) -> ActionAbstract:
        """génération de la bonne action selon le type

        Args:
            workflow_context (str): nom du context du workflow
            definition_dict (Dict[str, Any]): dictionnaire définissant l'action
            parent_action (Optional[&quot;ActionAbstract&quot;], optional): action précédente (si étape à plusieurs action). Defaults to None.
            behavior (Optional[str]): comportement à adopter si l'entité créée par l'action existe déjà sur l'entrepôt

        Returns:
            ActionAbstract: instance permettant de lancer l'action
        """
        if definition_dict["type"] == "processing-execution":
            return ProcessingExecutionAction(workflow_context, definition_dict, parent_action, behavior=behavior)
        if definition_dict["type"] == "configuration":
            return ConfigurationAction(workflow_context, definition_dict, parent_action)
        if definition_dict["type"] == "offering":
            return OfferingAction(workflow_context, definition_dict, parent_action)
        raise WorkflowError(f"Aucune correspondance pour ce type d'action : {definition_dict['type']}")

    @staticmethod
    def open_workflow(workflow_path: Path, workflow_name: Optional[str] = None) -> "Workflow":
        """Instancie un Workflow en vérifiant le schéma fourni.

        Args:
            workflow_path (Path): chemin vers le fichier de workflow.
            workflow_name (Optional[str], optional): nom du workflow, si None, le nom du fichier est utilisé. Defaults to None.

        Returns:
            Workflow: workflow instancié
        """
        # Chemin vers le schéma des workflows
        p_schema = Config.conf_dir_path / "json_schemas" / "workflow.json"
        # Vérification du schéma
        JsonHelper.validate_json(
            workflow_path,
            p_schema,
            schema_not_found_pattern="Le schéma décrivant la structure d'un workflow {schema_path} est introuvable. Contactez le support.",
            schema_not_parsable_pattern="Le schéma décrivant la structure d'un workflow {schema_path} est non parsable. Contactez le support.",
            schema_not_valid_pattern="Le schéma décrivant la structure d'un workflow {schema_path} est invalide. Contactez le support.",
            json_not_found_pattern="Le fichier de workflow {json_path} est introuvable. Contactez le support.",
            json_not_parsable_pattern="Le fichier de workflow {json_path} est non parsable. Contactez le support.",
            json_not_valid_pattern="Le fichier de workflow {json_path} est invalide. Contactez le support.",
        )
        # Ouverture du json
        d_workflow = JsonHelper.load(workflow_path)
        # Si le nom n'est pas défini, on prend celui du fichier
        if workflow_name is None:
            workflow_name = workflow_path.name
        # Instanciation et retour
        return Workflow(workflow_name, d_workflow)

    def validate(self) -> List[str]:
        """Valide le workflow en s'assurant qu'il est cohérent. Retourne la liste des erreurs trouvées.

        Returns:
            List[str]: liste des erreurs trouvées
        """
        l_errors: List[str] = []

        # Chemin vers le schéma des workflows
        p_schema = Config.conf_dir_path / "json_schemas" / "workflow.json"
        # Ouverture du schéma
        d_schema = JsonHelper.load(
            p_schema,
            file_not_found_pattern="Le schéma décrivant la structure d'un workflow {schema_path} est introuvable. Contactez le support.",
            file_not_parsable_pattern="Le schéma décrivant la structure d'un workflow {schema_path} est non parsable. Contactez le support.",
        )
        # Vérification du schéma
        try:
            jsonschema.validate(instance=self.__raw_definition_dict, schema=d_schema)
        # Récupération de l'erreur levée si le schéma est invalide
        except jsonschema.exceptions.SchemaError as e:
            raise GpfApiError(f"Le schéma décrivant la structure d'un workflow {p_schema} est invalide. Contactez le support.") from e
        # Récupération de l'erreur levée si le json est invalide
        except jsonschema.exceptions.ValidationError as e:
            l_errors.append(f"Le workflow ne respecte pas le schéma demandé. Erreur de schéma :\n--- début ---\n{e}\n--- fin ---")

        # Maintenant que l'on a fait ça, on peut faire des vérifications pratiques

        # 1. Est-ce que les parents de chaque étape existent ?
        # Pour chaque étape
        for s_step_name in self.steps:
            # Pour chaque parent de l'étape
            for s_parent_name in self.__get_step_definition(s_step_name)["parents"]:
                # S'il n'est pas dans la liste
                if not s_parent_name in self.steps:
                    l_errors.append(f"Le parent « {s_parent_name} » de l'étape « {s_step_name} » n'est pas défini dans le workflow.")

        # 2. Est-ce que chaque action a au moins une étape ?
        # Pour chaque étape
        for s_step_name in self.steps:
            # est-ce qu'il y a au moins une action ?
            if not self.__get_step_definition(s_step_name)["actions"]:
                l_errors.append(f"L'étape « {s_step_name} » n'a aucune action de défini.")

        # 3. Est-ce que chaque action de chaque étape est instantiable ?
        # Pour chaque étape
        for s_step_name in self.steps:
            # Pour chaque action de l'étape
            for i, d_action in enumerate(self.__get_step_definition(s_step_name)["actions"], 1):
                # On tente de l'instancier
                try:
                    Workflow.generate(self.name, d_action)
                except WorkflowError as e_workflow_error:
                    l_errors.append(f"L'action n°{i} de l'étape « {s_step_name} » n'est pas instantiable ({e_workflow_error}).")
                except KeyError as e_key_error:
                    l_errors.append(f"L'action n°{i} de l'étape « {s_step_name} » n'a pas la clef obligatoire ({e_key_error}).")
                except Exception as e:
                    l_errors.append(f"L'action n°{i} de l'étape « {s_step_name} » lève une erreur inattendue ({e}).")

        # On renvoie la liste
        return l_errors
