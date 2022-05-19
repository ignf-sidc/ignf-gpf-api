import json
from typing import Any, Dict, Optional, Type
import unittest
from unittest.mock import patch, MagicMock

from ignf_gpf_api.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.action.ConfigurationAction import ConfigurationAction
from ignf_gpf_api.action.GlobalResolver import GlobalResolver
from ignf_gpf_api.action.OfferingAction import OfferingAction
from ignf_gpf_api.action.ProcessingExecutionAction import ProcessingExecutionAction


# pylint:disable=too-many-arguments
# pylint:disable=too-many-locals
# pylint:disable=too-many-branches
# fmt: off
# (on désactive le formatage en attendant Python 3.10 et la possibilité de mettre des parenthèses pour gérer le multi with proprement)


# classe temporaire pour les test : ActionAbstract est abstraite
class ConcreteAction(ActionAbstract):
    def run(self) -> None:
        pass


class ActionAbstractTestCase(unittest.TestCase):
    """Tests UploadAction class.

    cmd : python3 -m unittest -b tests.action.ActionAbstractTestCase
    """


    def test_workflow_name(self) -> None:
        """test de workflow_name
        """
        d_definition ={"test": "val"}
        o_action = ConcreteAction("nom", d_definition, None)
        assert "nom" == o_action.workflow_name

    def test_definition_dict(self) -> None:
        """test de definition_dict
        """
        d_definition ={"test": "val"}
        o_action = ConcreteAction("nom", d_definition, None)
        assert d_definition == o_action.definition_dict

    def test_parent_action(self) -> None:
        """test de parent_action
        """
        d_definition ={"test": "val"}
        o_action = ConcreteAction("nom", d_definition, None)
        assert o_action.parent_action is None
        o_mock_parent = MagicMock()
        o_action = ConcreteAction("nom", d_definition, o_mock_parent)
        assert o_mock_parent == o_action.parent_action

    def test_resolve(self) -> None:
        """test de resolve
        """
        d_definition ={"test": "val"}
        d_resolved_dico = {"resolved": "val"}
        # on mock GlobalResolver
        with patch.object(GlobalResolver, "resolve", return_value=str(json.dumps(d_resolved_dico))) as o_mock_resolve :
            o_action = ConcreteAction("nom", d_definition, None)
            o_action.resolve()
            assert o_action.definition_dict == d_resolved_dico
            o_mock_resolve.assert_called_once_with(str(json.dumps(d_definition)))

    def run_generation(self, expected_type: Type["ActionAbstract"], name: str, dico_def: Dict[str, Any], parent: Optional["ActionAbstract"] = None) -> None:
        """lancement de la commande de génération

        Args:
            expected_type (Type[&quot;ActionAbstract&quot;]): type de la classe attendu en sortie de la fonction
            name (str): nom du workflow
            dico_def (Dict[str, Any]): dictionnaire de l'action
            parent (Optional[&quot;ActionAbstract&quot;], optional): parent de l'action. Defaults to None.
        """
        # mock des fonction __init__ des classes action généré
        def new_init(workflow_name: str, definition_dict: Dict[str, Any], parent_action: Optional["ActionAbstract"] = None) -> None:
            print ("new - ", workflow_name, definition_dict, parent_action)
        d_mock={}

        with patch.object(ProcessingExecutionAction, "__init__",  wraps=new_init) as d_mock["ProcessingExecutionAction"], \
            patch.object(ConfigurationAction, "__init__",  wraps=new_init) as d_mock["ConfigurationAction"], \
            patch.object(OfferingAction, "__init__",  wraps=new_init) as d_mock["OfferingAction"]:

            # exécution
            o_action_generated = ActionAbstract.generate(name, dico_def, parent)
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
