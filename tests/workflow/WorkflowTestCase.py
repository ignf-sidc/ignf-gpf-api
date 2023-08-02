from pathlib import Path
from typing import Any, Dict, Optional, Type, List, Callable
from unittest.mock import PropertyMock, patch, MagicMock

from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.helper.JsonHelper import JsonHelper
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.ProcessingExecution import ProcessingExecution

from ignf_gpf_api.workflow.Errors import WorkflowError
from ignf_gpf_api.workflow.Workflow import Workflow
from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.workflow.action.ConfigurationAction import ConfigurationAction
from ignf_gpf_api.workflow.action.OfferingAction import OfferingAction
from ignf_gpf_api.workflow.action.ProcessingExecutionAction import ProcessingExecutionAction

from tests.GpfTestCase import GpfTestCase

# pylint:disable=too-many-statements


class WorkflowTestCase(GpfTestCase):
    """Tests Workflow class.

    cmd : python3 -m unittest -b tests.workflow.WorkflowTestCase
    """

    o_mock_action = None

    def test_get_raw_dict(self) -> None:
        """test de get_raw_dict"""
        d_workflow = {"test": "val"}
        o_workflow = Workflow("nom", d_workflow)
        self.assertDictEqual(d_workflow, o_workflow.get_raw_dict())

    def run_run_step(
        self,
        s_etape: str,
        s_datastore: Optional[str],
        d_workflow: Dict[str, Any],
        l_run_args: List[Any],
        callback: Optional[Callable[[ProcessingExecution], None]] = None,
        behavior: Optional[str] = None,
        monitoring_until_end: Optional[List[str]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        """Fonction de lancement des tests pour run_step()

        Args:
            s_etape (str): nom de l'étape du workflow à lancé
            s_datastore (Optional[str]): nom du datastore à utiliser, si None datastore trouvé dans l'étape, le workflow ou None.
            d_workflow (Dict[str, Any]): dictionnaire du workflow
            l_run_args (List[Any]): liste des argument passé en appel de action.run(). Un élément = un appel
            callback (Optional[Callable[[ProcessingExecution], None]], optional): possible callback utilisé. Defaults to None.
            behavior (Optional[str], optional): Action en cas de doublon, None action par défaut. Defaults to None.
            monitoring_until_end (Optional[List[str]], optional): si None, action sans monitoring, si défini : définition du side effect du mock de action.monitoring_until_end(). Defaults to None.
            error_message (Optional[str], optional): Message d'erreur compléter avec "action", si None : pas d'erreur attendu. Defaults to None.
        """
        # récupération de la liste d'action
        l_actions = []
        if s_etape in d_workflow["workflow"]["steps"]:
            l_actions = d_workflow["workflow"]["steps"][s_etape]["actions"]

        # création du o_mock_action
        if monitoring_until_end:
            # cas avec monitoring
            o_mock_action = MagicMock(spec=ProcessingExecutionAction)
            o_mock_action.monitoring_until_end.side_effect = monitoring_until_end
            o_mock_action.stored_data = "entite"
            o_mock_action.upload = None

        else:
            # cas sans monitoring
            o_mock_action = MagicMock(spec=ConfigurationAction)
            o_mock_action.configuration = "entite"
        ## config mock générale
        o_mock_action.resolve.return_value = None
        o_mock_action.run.return_value = None
        ## mock de la property definition_dict
        if len(l_actions) == 1:
            type(o_mock_action).definition_dict = PropertyMock(return_value=l_actions[0])
        else:
            d_effect = []
            for d_el in l_actions:
                d_effect += [d_el] * 2
            type(o_mock_action).definition_dict = PropertyMock(side_effect=d_effect)

        # initialisation de Workflow
        o_workflow = Workflow("nom", d_workflow)

        # on mock Workflow.generate
        with patch.object(Workflow, "generate", return_value=o_mock_action) as o_mock_action_generate:
            if error_message is not None:
                # si on attend une erreur
                with self.assertRaises(WorkflowError) as o_arc:
                    o_workflow.run_step(s_etape, callback, behavior, s_datastore)
                self.assertEqual(o_arc.exception.message, error_message.format(action=o_mock_action))
            else:
                # pas d'erreur attendu
                l_entities = o_workflow.run_step(s_etape, callback, behavior, s_datastore)
                self.assertListEqual(l_entities, ["entite"] * len(l_run_args))

            # vérification des appels à generate
            self.assertEqual(o_mock_action_generate.call_count, len(l_run_args))
            o_parent = None
            for i in range(len(l_run_args)):
                o_mock_action_generate.assert_any_call(s_etape, l_actions[i], o_parent, behavior)
                o_parent = o_mock_action

            # vérification des appels à résolve
            self.assertEqual(o_mock_action.resolve.call_count, len(l_run_args))

            # vérification des appels à run
            self.assertEqual(o_mock_action.run.call_count, len(l_run_args))
            for o_el in l_run_args:
                o_mock_action.run.assert_any_call(o_el)

            # si monitoring : vérification des appels à monitoring
            if monitoring_until_end:
                self.assertEqual(o_mock_action.resolve.call_count, len(l_run_args))
                o_mock_action.monitoring_until_end.assert_any_call(callback=callback)

    def test_run_step(self) -> None:
        """test de run_step"""

        # fonction callback
        def callback(o_pe: ProcessingExecution) -> None:
            """fonction bidon pour affichage le traitement

            Args:
                o_pe (ProcessingExecution): traitement dont on suit le traitement
            """
            print(o_pe)

        d_workflow: Dict[str, Any] = {
            "workflow": {
                "steps": {
                    "1er etape": {},
                    "autre": {},
                    "mise-en-base": {
                        "actions": [{"type": "action1"}],
                    },
                    "mise-en-base2": {
                        "actions": [{"type": "action2-1"}, {"type": "action2-2"}],
                    },
                    "mise-en-base3": {
                        "actions": [{"type": "action3", "datastore": "datastore_3"}],
                    },
                    "mise-en-base4": {
                        "actions": [{"type": "action4-1", "datastore": "datastore_4-1"}, {"type": "action4-2"}],
                    },
                }
            }
        }
        d_workflow_2: Dict[str, Any] = {"datastore": "datastore_workflow", **d_workflow}
        s_datastore = "datastore_force"

        # test simple sans s_datastore
        self.run_run_step("mise-en-base", None, d_workflow, [None])
        self.run_run_step("mise-en-base2", None, d_workflow, [None, None])

        # datastore au niveau des étapes
        self.run_run_step("mise-en-base3", None, d_workflow, ["datastore_3"])
        self.run_run_step("mise-en-base4", None, d_workflow, ["datastore_4-1", None])

        # datastore au niveau du workflow + étapes
        self.run_run_step("mise-en-base", None, d_workflow_2, ["datastore_workflow"])
        self.run_run_step("mise-en-base3", None, d_workflow_2, ["datastore_3"])
        self.run_run_step("mise-en-base4", None, d_workflow_2, ["datastore_4-1", "datastore_workflow"])

        # datastore au niveau du workflow + étape + forcé dans l'appel
        self.run_run_step("mise-en-base", s_datastore, d_workflow, [s_datastore])
        self.run_run_step("mise-en-base", s_datastore, d_workflow_2, [s_datastore])
        self.run_run_step("mise-en-base3", s_datastore, d_workflow_2, [s_datastore])
        self.run_run_step("mise-en-base4", s_datastore, d_workflow_2, [s_datastore, s_datastore])

        # étape qui n'existe pas
        self.run_run_step("existe_pas", None, d_workflow, [], error_message="L'étape existe_pas n'est pas définie dans le workflow nom")
        # test avec monitoring
        self.run_run_step("mise-en-base", None, d_workflow, [None], monitoring_until_end=["SUCCESS"])
        self.run_run_step("mise-en-base", None, d_workflow, [None], monitoring_until_end=["FAILURE"], error_message="L'exécution de traitement {action} ne s'est pas bien passée. Sortie FAILURE.")
        self.run_run_step("mise-en-base", None, d_workflow, [None], monitoring_until_end=["ABORTED"], error_message="L'exécution de traitement {action} ne s'est pas bien passée. Sortie ABORTED.")
        self.run_run_step(
            "mise-en-base4",
            None,
            d_workflow_2,
            ["datastore_4-1", "datastore_workflow"],
            monitoring_until_end=["SUCCESS", "ABORTED"],
            error_message="L'exécution de traitement {action} ne s'est pas bien passée. Sortie ABORTED.",
        )
        self.run_run_step("mise-en-base4", None, d_workflow_2, ["datastore_4-1", "datastore_workflow"], monitoring_until_end=["SUCCESS", "SUCCESS"])
        # callbable
        self.run_run_step("mise-en-base", None, d_workflow, [None], callback, None, ["SUCCESS"])
        # behavior
        self.run_run_step("mise-en-base", None, d_workflow, [None], None, "DELETE")
        self.run_run_step("mise-en-base", None, d_workflow, [None], callback, "DELETE", ["SUCCESS"])

    def run_generation(self, expected_type: Type[ActionAbstract], name: str, dico_def: Dict[str, Any], parent: Optional[ActionAbstract] = None, behavior: Optional[str] = None) -> None:
        """lancement de la commande de génération

        Args:
            expected_type (Type[ActionAbstract]): type de la classe attendu en sortie de la fonction
            name (str): nom du contexte du workflow
            dico_def (Dict[str, Any]): dictionnaire de l'action
            parent (Optional[ActionAbstract], optional): parent de l'action.
            behavior (Optional[str], optional): comportement à adopter.
        """

        # mock des fonction __init__ des classes action généré
        def new_init(workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional[ActionAbstract] = None, behavior: Optional[str] = None) -> None:
            print("new - ", workflow_context, definition_dict, parent_action, behavior)

        d_mock = {}

        with patch.object(ProcessingExecutionAction, "__init__", wraps=new_init) as d_mock["ProcessingExecutionAction"]:
            with patch.object(ConfigurationAction, "__init__", wraps=new_init) as d_mock["ConfigurationAction"]:
                with patch.object(OfferingAction, "__init__", wraps=new_init) as d_mock["OfferingAction"]:
                    # exécution
                    o_action_generated = Workflow.generate(name, dico_def, parent, behavior=behavior)
                    # tests
                    self.assertIsInstance(o_action_generated, expected_type)
                    for s_class_name, o_mock in d_mock.items():
                        if expected_type.__name__ == s_class_name:
                            # Le comportement n'est transmis que pour les ProcessingExecutionAction (pour le moment)
                            if isinstance(o_action_generated, ProcessingExecutionAction):
                                o_mock.assert_called_once_with(name, dico_def, parent, behavior=behavior)
                            else:
                                o_mock.assert_called_once_with(name, dico_def, parent)
                        else:
                            o_mock.assert_not_called()

    def test_generate(self) -> None:
        """test de generate"""
        # mock pour les parents
        o_mock_parent = MagicMock()

        # test type processing-execution
        self.run_generation(ProcessingExecutionAction, "name", {"type": "processing-execution"}, None, behavior="DELETE")
        self.run_generation(ProcessingExecutionAction, "name", {"type": "processing-execution"}, o_mock_parent)

        # test type configuration
        self.run_generation(ConfigurationAction, "name", {"type": "configuration"}, None, behavior="DELETE")
        self.run_generation(ConfigurationAction, "name", {"type": "configuration"}, o_mock_parent)

        # test type offering
        self.run_generation(OfferingAction, "name", {"type": "offering"}, None, behavior="DELETE")
        self.run_generation(OfferingAction, "name", {"type": "offering"}, o_mock_parent)

    def test_open_workflow(self) -> None:
        """Test de la fonction open_workflow."""
        p_workflows = Config().data_dir_path / "workflows"
        # On teste le workflow generic_archive.jsonc
        o_workflow_1 = Workflow.open_workflow(p_workflows / "generic_archive.jsonc")
        self.assertEqual(o_workflow_1.name, "generic_archive.jsonc")
        self.assertEqual(len(o_workflow_1.steps), 3)
        # On teste le workflow generic_vecteur.jsonc
        o_workflow_2 = Workflow.open_workflow(p_workflows / "generic_vecteur.jsonc", "wfs generic")
        self.assertEqual(o_workflow_2.name, "wfs generic")
        self.assertEqual(len(o_workflow_2.steps), 8)
        # On teste un fichier inexistant
        with self.assertRaises(GpfApiError) as o_arc:
            Workflow.open_workflow(Path("pas_là.json"))
        self.assertEqual(o_arc.exception.message, "Le fichier de workflow pas_là.json est introuvable. Contactez le support.")

    def test_validate(self) -> None:
        """Test de la fonction validate."""
        p_workflows = Config.data_dir_path / "workflows"
        # On valide le workflow generic_archive.jsonc
        o_workflow_1 = Workflow.open_workflow(p_workflows / "generic_archive.jsonc")
        self.assertFalse(o_workflow_1.validate())
        # On valide le workflow generic_vecteur.jsonc
        o_workflow_2 = Workflow.open_workflow(p_workflows / "generic_vecteur.jsonc")
        self.assertFalse(o_workflow_2.validate())
        # On ne valide pas le workflow bad-workflow.jsonc
        p_workflow = GpfTestCase.data_dir_path / "workflows" / "bad-workflow.jsonc"
        o_workflow_2 = Workflow(p_workflow.stem, JsonHelper.load(p_workflow))
        l_errors = o_workflow_2.validate()
        self.assertTrue(l_errors)
        self.assertIn("Le workflow ne respecte pas le schéma demandé. Erreur de schéma :", l_errors[0])
        self.assertEqual(l_errors[1], "Le parent « parent-not-found » de l'étape « no-parent-no-action » n'est pas défini dans le workflow.")
        self.assertEqual(l_errors[2], "L'étape « no-parent-no-action » n'a aucune action de défini.")
        self.assertEqual(l_errors[3], "L'action n°1 de l'étape « configuration-wfs » n'est pas instantiable (Aucune correspondance pour ce type d'action : type-not-found).")
        self.assertEqual(l_errors[4], "L'action n°2 de l'étape « configuration-wfs » n'a pas la clef obligatoire ('type').")

    def test_get_actions(self) -> None:
        """Test de get_actions."""
        # Données test
        d_action_0 = {"type": "action_0"}
        d_action_1 = {"type": "action_1"}
        d_action_2 = {"type": "action_2"}
        d_workflow = {
            "workflow": {
                "steps": {
                    "step_name": {
                        "actions": [
                            d_action_0,
                            d_action_1,
                            d_action_2,
                        ],
                    },
                }
            }
        }
        l_actions = ["action_0", "action_1", "action_2"]
        # Instanciation workflow
        o_workflow = Workflow("workflow_name", d_workflow)
        # On mock generate
        with patch.object(Workflow, "generate", side_effect=l_actions) as o_mock_generate:
            # Appel fonction testée
            l_action_get = o_workflow.get_actions("step_name")
            # Vérification
            self.assertListEqual(l_actions, l_action_get)
            self.assertEqual(o_mock_generate.call_count, 3)
            o_mock_generate.assert_any_call("step_name", d_action_0, None)
            o_mock_generate.assert_any_call("step_name", d_action_1, "action_0")
            o_mock_generate.assert_any_call("step_name", d_action_2, "action_1")

    def test_get_action(self) -> None:
        """Test de get_action."""
        # Données test
        l_actions = ["action_0", "action_1", "action_2"]
        # Instanciation workflow
        o_workflow = Workflow("workflow_name", {})
        # On demande l'action i
        for i, o_action in enumerate(l_actions):
            with patch.object(o_workflow, "get_actions", return_value=l_actions) as o_mock_get_actions:
                # Appel fonction testée
                o_action_get = o_workflow.get_action("stem_name", i)
                # Vérifications
                self.assertEqual(o_action, o_action_get)
                o_mock_get_actions.assert_called_once_with("stem_name")
