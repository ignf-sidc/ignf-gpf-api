from pathlib import Path
from typing import Any, Dict, Optional, Type
from unittest.mock import patch, MagicMock

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

    def test_get_raw_dict(self) -> None:
        """test de get_raw_dict"""
        d_workflow = {"test": "val"}
        o_workflow = Workflow("nom", d_workflow)
        self.assertDictEqual(d_workflow, o_workflow.get_raw_dict())

    def test_run_step(self) -> None:
        """test de run_step"""
        d_workflow = {
            "workflow": {
                "steps": {
                    "1er etape": {},
                    "autre": {},
                    "mise-en-base": {
                        "actions": [
                            {
                                "type": "action1",
                            }
                        ],
                    },
                    "mise-en-base2": {
                        "actions": [
                            {
                                "type": "action2-1",
                            },
                            {
                                "type": "action2-2",
                            },
                        ],
                    },
                }
            }
        }
        o_workflow = Workflow("nom", d_workflow)
        # l'étape n'existe pas : ça plante.
        with self.assertRaises(WorkflowError) as o_arc:
            o_workflow.run_step("existe_pas")
        self.assertEqual(o_arc.exception.message, "L'étape existe_pas n'est pas définie dans le workflow nom")

        o_mock_action = MagicMock()
        o_mock_action.resolve.return_value = None
        o_mock_action.run.return_value = None
        # on mock Workflow.generate
        with patch.object(Workflow, "generate", return_value=o_mock_action) as o_mock_action_generate:
            # test pour une action
            o_workflow.run_step("mise-en-base")
            o_mock_action.run.assert_called_once_with()
            o_mock_action_generate.assert_called_once_with("mise-en-base", {"type": "action1"}, None, None)
            o_mock_action.resolve.assert_called_once_with()
            o_mock_action.run.assert_called_once_with()

            # reset des mock
            o_mock_action_generate.reset_mock()
            o_mock_action.reset_mock()

            # test pour 2 actions
            o_workflow.run_step("mise-en-base2")
            self.assertEqual(o_mock_action_generate.call_count, 2)
            o_mock_action_generate.assert_any_call("mise-en-base2", {"type": "action2-1"}, None, None)
            o_mock_action_generate.assert_any_call("mise-en-base2", {"type": "action2-2"}, o_mock_action, None)
            self.assertEqual(o_mock_action.resolve.call_count, 2)
            self.assertEqual(o_mock_action.run.call_count, 2)

        # test pour ProcessingExecutionAction

        # fonction callback
        def callback(o_pe: ProcessingExecution) -> None:
            """fonction bidon pour affichage le traitement

            Args:
                o_pe (ProcessingExecution): traitement dont on suit le traitement
            """
            print(o_pe)

        # reset / config des mock
        o_mock_action_generate.reset_mock()

        o_mock_processing_execution_action = MagicMock(spec=ProcessingExecutionAction)
        o_mock_processing_execution_action.resolve.return_value = None
        o_mock_processing_execution_action.run.return_value = None

        with patch.object(Workflow, "generate", return_value=o_mock_processing_execution_action) as o_mock_action_generate:
            # sortie en success
            o_mock_processing_execution_action.monitoring_until_end.return_value = "SUCCESS"
            o_workflow.run_step("mise-en-base")
            o_mock_processing_execution_action.run.assert_called_once_with()
            o_mock_action_generate.assert_called_once_with("mise-en-base", {"type": "action1"}, None, None)
            o_mock_processing_execution_action.resolve.assert_called_once_with()
            o_mock_processing_execution_action.run.assert_called_once_with()
            o_mock_processing_execution_action.monitoring_until_end.assert_called_once_with(callback=None)

            # reset des mock
            o_mock_action_generate.reset_mock()
            o_mock_processing_execution_action.reset_mock()

            # sortie en success avec callback
            o_mock_processing_execution_action.monitoring_until_end.return_value = "SUCCESS"
            o_workflow.run_step("mise-en-base", callback)
            o_mock_processing_execution_action.run.assert_called_once_with()
            o_mock_action_generate.assert_called_once_with("mise-en-base", {"type": "action1"}, None, None)
            o_mock_processing_execution_action.resolve.assert_called_once_with()
            o_mock_processing_execution_action.run.assert_called_once_with()
            o_mock_processing_execution_action.monitoring_until_end.assert_called_once_with(callback=callback)

            # reset des mock
            o_mock_action_generate.reset_mock()
            o_mock_processing_execution_action.reset_mock()

            # sortie en FAILURE
            o_mock_processing_execution_action.monitoring_until_end.return_value = "FAILURE"
            with self.assertRaises(WorkflowError) as o_arc:
                o_workflow.run_step("mise-en-base")
            self.assertEqual(o_arc.exception.message, f"Le ProcessingExecution {o_mock_processing_execution_action} ne s'est pas bien passé. Sortie FAILURE")

            # reset des mock
            o_mock_action_generate.reset_mock()
            o_mock_processing_execution_action.reset_mock()

            # sortie en ABORTED
            o_mock_processing_execution_action.monitoring_until_end.return_value = "ABORTED"
            with self.assertRaises(WorkflowError) as o_arc:
                o_workflow.run_step("mise-en-base")
            self.assertEqual(o_arc.exception.message, f"Le ProcessingExecution {o_mock_processing_execution_action} ne s'est pas bien passé. Sortie ABORTED")

    def run_generation(self, expected_type: Type[ActionAbstract], name: str, dico_def: Dict[str, Any], parent: Optional[ActionAbstract] = None, behavior: Optional[str] = None) -> None:
        """lancement de la commande de génération

        Args:
            expected_type (Type[ActionAbstract]): type de la classe attendu en sortie de la fonction
            name (str): nom du contexte du workflow
            dico_def (Dict[str, Any]): dictionnaire de l'action
            parent (Optional[ActionAbstract], optional): parent de l'action. Defaults to None.
            behavior (Optional[str], optional): comportement à adopter. Defaults to None.
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
        # On teste le workflow archive-generic.jsonc
        o_workflow_1 = Workflow.open_workflow(p_workflows / "archive-generic.jsonc")
        self.assertEqual(o_workflow_1.name, "archive-generic.jsonc")
        self.assertEqual(len(o_workflow_1.steps), 3)
        # On teste le workflow wfs-generic.jsonc
        o_workflow_2 = Workflow.open_workflow(p_workflows / "wfs-generic.jsonc", "wfs generic")
        self.assertEqual(o_workflow_2.name, "wfs generic")
        self.assertEqual(len(o_workflow_2.steps), 4)
        # On teste un fichier inexistant
        with self.assertRaises(GpfApiError) as o_arc:
            Workflow.open_workflow(Path("pas_là.json"))
        self.assertEqual(o_arc.exception.message, "Le fichier de workflow pas_là.json est introuvable. Contactez le support.")

    def test_validate(self) -> None:
        """Test de la fonction validate."""
        p_workflows = Config.data_dir_path / "workflows"
        # On valide le workflow archive-generic.jsonc
        o_workflow_1 = Workflow.open_workflow(p_workflows / "archive-generic.jsonc")
        self.assertFalse(o_workflow_1.validate())
        # On valide le workflow wfs-generic.jsonc
        o_workflow_2 = Workflow.open_workflow(p_workflows / "wfs-generic.jsonc")
        self.assertFalse(o_workflow_2.validate())
        # On valide le workflow bad-workflow.jsonc
        p_workflow = GpfTestCase.data_dir_path / "workflows" / "bad-workflow.jsonc"
        o_workflow_2 = Workflow(p_workflow.stem, JsonHelper.load(p_workflow))
        l_errors = o_workflow_2.validate()
        self.assertTrue(l_errors)
        self.assertIn("Le workflow ne respecte pas le schéma demandé. Erreur de schéma :", l_errors[0])
        self.assertEqual(l_errors[1], "Le parent « parent-not-found » de l'étape « no-parent-no-action » n'est pas défini dans le workflow.")
        self.assertEqual(l_errors[2], "L'étape « no-parent-no-action » n'a aucune action de défini.")
        self.assertEqual(l_errors[3], "L'action n°1 de l'étape « configuration-wfs » n'est pas instantiable (Aucune correspondance pour ce type d'action : type-not-found).")
        self.assertEqual(l_errors[4], "L'action n°2 de l'étape « configuration-wfs » n'a pas la clef obligatoire ('type').")
