import json
from unittest.mock import patch, MagicMock

from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.workflow.resolver.GlobalResolver import GlobalResolver
from tests.GpfTestCase import GpfTestCase


# classe temporaire pour les test : ActionAbstract est abstraite
class ConcreteAction(ActionAbstract):
    def run(self) -> None:
        pass


class ActionAbstractTestCase(GpfTestCase):
    """Tests ActionAbstract class.

    cmd : python3 -m unittest -b tests.workflow.action.ActionAbstractTestCase
    """

    def test_workflow_context(self) -> None:
        """test de workflow_context"""
        d_definition = {"test": "val"}
        o_action = ConcreteAction("nom", d_definition, None)
        assert "nom" == o_action.workflow_context

    def test_definition_dict(self) -> None:
        """test de definition_dict"""
        d_definition = {"test": "val"}
        o_action = ConcreteAction("nom", d_definition, None)
        assert d_definition == o_action.definition_dict

    def test_parent_action(self) -> None:
        """test de parent_action"""
        d_definition = {"test": "val"}
        o_action = ConcreteAction("nom", d_definition, None)
        assert o_action.parent_action is None
        o_mock_parent = MagicMock()
        o_action = ConcreteAction("nom", d_definition, o_mock_parent)
        assert o_mock_parent == o_action.parent_action

    def test_resolve(self) -> None:
        """test de resolve"""
        d_definition = {"test": "val"}
        d_resolved_dico = {"resolved": "val"}
        # on mock GlobalResolver
        with patch.object(GlobalResolver, "resolve", return_value=str(json.dumps(d_resolved_dico))) as o_mock_resolve:
            o_action = ConcreteAction("nom", d_definition, None)
            o_action.resolve()
            assert o_action.definition_dict == d_resolved_dico
            o_mock_resolve.assert_called_once_with(str(json.dumps(d_definition, indent=4)))
