from typing import Any, Dict, Optional, Type
import unittest
from unittest.mock import patch, MagicMock

from ignf_gpf_api.action.Errors import WorkflowError
from ignf_gpf_api.action.Workflow import Workflow

from ignf_gpf_api.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.action.ConfigurationAction import ConfigurationAction
from ignf_gpf_api.action.OfferingAction import OfferingAction
from ignf_gpf_api.action.ProcessingExecutionAction import ProcessingExecutionAction


# pylint:disable=too-many-arguments
# pylint:disable=too-many-locals
# pylint:disable=too-many-branches
# fmt: off
# (on désactive le formatage en attendant Python 3.10 et la possibilité de mettre des parenthèses pour gérer le multi with proprement)


class WorkflowTestCase(unittest.TestCase):
    """Tests UploadAction class.

    cmd : python3 -m unittest -b tests.action.WorkflowTestCase
    """

    def test_get_raw_dict(self) -> None:
        """test de get_raw_dict
        """
        d_workflow ={"test": "val"}
        o_workflow = Workflow("nom", d_workflow)
        self.assertDictEqual(d_workflow, o_workflow.get_raw_dict())

    def test_run_step(self) -> None:
        """test de run_step
        """
        d_workflow = {"workflow": {
            "steps": [{
                "name":"1er etape"
            },{
                "name":"autre"
            },{
                "name": "mise-en-base",
                "actions": [
                    {
                        "type": "action1",
                    }
                ]
            },{
                "name": "mise-en-base2",
                "actions": [
                    {
                        "type": "action2-1",
                    },{
                        "type": "action2-2",
                    }
                ]
            }]
        }}
        o_workflow = Workflow("nom", d_workflow)
        # l'étape n'existe pas : ça plante.
        with self.assertRaises(WorkflowError) as o_arc:
            o_workflow.run_step("existe_pas")
        self.assertEqual(o_arc.exception.message, "L'étape existe_pas n'est pas définie dans le workflow nom")

        o_mock_action = MagicMock()
        o_mock_action.resolve.return_value = None
        o_mock_action.run.return_value = None
        # on mock Workflow.generate
        with patch.object(Workflow, "generate", return_value=o_mock_action) as o_mock_action_generate :
            # test pour une action
            o_workflow.run_step("mise-en-base")
            o_mock_action.run.assert_called_once()
            o_mock_action_generate.assert_called_once_with('mise-en-base/action1', {'type': 'action1'}, None)
            o_mock_action.resolve.assert_called_once_with()
            o_mock_action.run.assert_called_once_with()

            # reset des mock
            o_mock_action_generate.reset_mock()
            o_mock_action.reset_mock()

            # test pour 2 actions
            o_workflow.run_step("mise-en-base2")
            self.assertEqual(o_mock_action_generate.call_count, 2)
            o_mock_action_generate.assert_any_call('mise-en-base2/action2-1', {'type': 'action2-1'}, None)
            o_mock_action_generate.assert_any_call('mise-en-base2/action2-2', {'type': 'action2-2'}, o_mock_action)
            self.assertEqual(o_mock_action.resolve.call_count, 2)
            self.assertEqual(o_mock_action.run.call_count, 2)

    def run_generation(self, expected_type: Type[ActionAbstract], name: str, dico_def: Dict[str, Any], parent: Optional[ActionAbstract] = None) -> None:
        """lancement de la commande de génération

        Args:
            expected_type (Type[&quot;ActionAbstract&quot;]): type de la classe attendu en sortie de la fonction
            name (str): nom du contexte du workflow
            dico_def (Dict[str, Any]): dictionnaire de l'action
            parent (Optional[&quot;ActionAbstract&quot;], optional): parent de l'action. Defaults to None.
        """
        # mock des fonction __init__ des classes action généré
        def new_init(workflow_context: str, definition_dict: Dict[str, Any], parent_action: Optional[ActionAbstract] = None) -> None:
            print ("new - ", workflow_context, definition_dict, parent_action)
        d_mock={}

        with patch.object(ProcessingExecutionAction, "__init__",  wraps=new_init) as d_mock["ProcessingExecutionAction"], \
            patch.object(ConfigurationAction, "__init__",  wraps=new_init) as d_mock["ConfigurationAction"], \
            patch.object(OfferingAction, "__init__",  wraps=new_init) as d_mock["OfferingAction"]:

            # exécution
            o_action_generated = Workflow.generate(name, dico_def, parent)
            # testes
            assert type(o_action_generated) == expected_type

            for s_class_name, o_mock in d_mock.items():
                if expected_type.__name__ == s_class_name:
                    o_mock.assert_called_once_with(name, dico_def, parent)
                else:
                    o_mock.assert_not_called()

    def test_generate(self) -> None:
        """test de generate
        """
        # mock pour les parents
        o_mock_parent = MagicMock()

        # test type processing-execution
        self.run_generation(ProcessingExecutionAction, "name", {"type": "processing-execution"}, None)
        self.run_generation(ProcessingExecutionAction, "name", {"type": "processing-execution"}, o_mock_parent)

        # test type configuration
        self.run_generation(ConfigurationAction, "name", {"type": "configuration"}, None)
        self.run_generation(ConfigurationAction, "name", {"type": "configuration"}, o_mock_parent)

        # test type offering
        self.run_generation(OfferingAction, "name", {"type": "offering"}, None)
        self.run_generation(OfferingAction, "name", {"type": "offering"}, o_mock_parent)
