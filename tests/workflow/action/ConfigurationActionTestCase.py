from typing import Any, Dict, List, Optional

from unittest.mock import patch, MagicMock

from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.workflow.action.ConfigurationAction import ConfigurationAction
from tests.GpfTestCase import GpfTestCase


# pylint:disable=too-many-arguments
# pylint:disable=too-many-locals
# pylint:disable=too-many-branches
# fmt: off
class ConfigurationActionTestCase(GpfTestCase):
    """Tests ConfigurationAction class.

    cmd : python3 -m unittest -b tests.workflow.action.ConfigurationActionTestCase
    """

    def run_args(self, tags: Optional[Dict[str, Any]], comments: Optional[List[str]]) -> None:
        """lancement +test de ConfigurationAction.run selon param
        Args:
            tags (Optional[Dict[str, Any]]): dict des tags ou None
            comments (Optional[List]): list des comments ou None
        """
        # creation du dictionnaire qui reprend les paramètres du workflow pour créer une configuration
        d_action = {"type": "configuration", "body_parameters": {"param": "valeur"}}
        if tags is not None:
            d_action["tags"] = tags
        if comments is not None:
            d_action["comments"] = comments

        # initialisation de Configuration
        o_conf = ConfigurationAction("contexte", d_action)

        # mock de configuration
        o_mock_configuration = MagicMock()
        o_mock_configuration.api_launch.return_value = None


        # suppression de la mise en page forcé pour le with
        with patch.object(Configuration, "api_create", return_value=o_mock_configuration) as o_mock_configuration_api_create :
            # on lance l'exécution de run
            o_conf.run()

            # test de l'appel à Configuration.api_create
            o_mock_configuration_api_create.assert_called_once_with(d_action['body_parameters'])

            # test api_add_tags
            if "tags" in d_action and d_action["tags"]:
                o_mock_configuration.api_add_tags.assert_called_once_with(d_action["tags"])
            else:
                o_mock_configuration.api_add_tags.assert_not_called()

            # test commentaires
            if "comments" in d_action and d_action["comments"]:
                self.assertEqual(len(d_action["comments"]), o_mock_configuration.api_add_comment.call_count)
                for s_comm in d_action["comments"]:
                    o_mock_configuration.api_add_comment.assert_any_call({"text": s_comm})
            else:
                o_mock_configuration.api_add_comment.assert_not_called()

    def test_run(self) -> None:
        """test de run"""
        ## sans tag + sans commentaire
        self.run_args(None, None)
        ## tag vide + commentaire vide
        self.run_args({}, [])
        ## 1 tag + 1 commentaire
        self.run_args({"tag1": "val1"}, ["comm1"])
        ## 2 tag + 4 commentaire
        self.run_args({"tag1": "val1", "tag2": "val2"}, ["comm1", "comm2", "comm3", "comm4"])
