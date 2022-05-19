import unittest
from unittest.mock import patch, MagicMock
from ignf_gpf_api.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.action.Errors import WorkflowError

from ignf_gpf_api.action.Workflow import Workflow


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
        assert d_workflow == o_workflow.get_raw_dict()

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
            o_workflow.run_step("n existe pas")
        self.assertEqual(o_arc.exception.message, "L'étape n existe pas n'est pas définie dans le workflow nom")

        o_mock_action = MagicMock()
        o_mock_action.resolve.return_value = None
        o_mock_action.run.return_value = None
        # on mock ActionAbstract
        with patch.object(ActionAbstract, "generate", return_value=o_mock_action) as o_mock_action_generate :
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
            assert o_mock_action_generate.call_count == 2
            o_mock_action_generate.assert_any_call('mise-en-base2/action2-1', {'type': 'action2-1'}, None)
            o_mock_action_generate.assert_any_call('mise-en-base2/action2-2', {'type': 'action2-2'}, o_mock_action)
            assert o_mock_action.resolve.call_count == 2
            assert o_mock_action.run.call_count == 2
