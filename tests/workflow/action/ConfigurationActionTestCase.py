from typing import Any, Dict, List, Optional

from unittest.mock import patch, MagicMock

from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.workflow.action.ActionAbstract import ActionAbstract
from ignf_gpf_api.workflow.action.ConfigurationAction import ConfigurationAction
from tests.GpfTestCase import GpfTestCase


# pylint:disable=too-many-arguments
# pylint:disable=too-many-locals
# pylint:disable=too-many-branches


class ConfigurationActionTestCase(GpfTestCase):
    """Tests ConfigurationAction class.

    cmd : python3 -m unittest -b tests.workflow.action.ConfigurationActionTestCase
    """

    def test_find_configuration(self) -> None:
        """Test find_configuration.

        Dans ce test, on suppose que le datastore est défini (cf. find_configuration).
        """
        o_c1 = Configuration({"_id": "pe_1"})
        o_c2 = Configuration({"_id": "pe_2"})
        # création du dict décrivant l'action
        d_action: Dict[str, Any] = {
            "type": "configuration",
            "body_parameters": {
                "name": "name_configuration",
                "layer_name": "layer_name_configuration",
            },
            "tags": {
                "tag": "val",
            },
        }
        # exécution de ConfigurationAction
        o_ca = ConfigurationAction("contexte", d_action)
        # Mock de ActionAbstract.get_filters et Configuration.api_list
        with patch.object(ActionAbstract, "get_filters", return_value=({"info": "val"}, {"tag": "val"})) as o_mock_get_filters:
            with patch.object(Configuration, "api_list", return_value=[o_c1, o_c2]) as o_mock_api_list:
                # Appel de la fonction find_configuration
                o_stored_data = o_ca.find_configuration("datastore_id")
                # Vérifications
                o_mock_get_filters.assert_called_once_with("configuration", d_action["body_parameters"], d_action["tags"])
                o_mock_api_list.assert_called_once_with(infos_filter={"info": "val"}, tags_filter={"tag": "val"}, datastore="datastore_id")
                self.assertEqual(o_stored_data, o_c1)

    def run_args(
        self,
        tags: Optional[Dict[str, Any]],
        comments: Optional[List[str]],
        config_already_exists: bool,
        comment_exist: bool = False,
    ) -> None:
        """lancement +test de ConfigurationAction.run selon param
        Args:
            tags (Optional[Dict[str, Any]]): dict des tags ou None
            comments (Optional[List[str]]): liste des comments ou None
            config_already_exists (bool): configuration déjà existante
            comment_exist (bool): si on a un commentaire qui existe déjà
        """
        # creation du dictionnaire qui reprend les paramètres du workflow pour créer une configuration
        d_action: Dict[str, Any] = {"type": "configuration", "body_parameters": {"param": "valeur"}}
        if tags is not None:
            d_action["tags"] = tags
        if comments is not None:
            d_action["comments"] = comments.copy()
            if comment_exist:
                d_action["comments"].append("commentaire existe")

        # mock de configuration
        o_mock_configuration = MagicMock()
        o_mock_configuration.api_launch.return_value = None
        o_mock_configuration.api_add_comment.return_value = None
        o_mock_configuration.api_list_comments.return_value = [{"text": "commentaire existe"}] if comment_exist else []

        # Liste des configurations déjà existantes
        if config_already_exists:
            l_configs = [o_mock_configuration]
        else:
            l_configs = []

        # suppression de la mise en page forcé pour le with
        with patch.object(Configuration, "api_create", return_value=o_mock_configuration) as o_mock_configuration_api_create:
            with patch.object(Configuration, "api_list", return_value=l_configs) as o_mock_configuration_api_list:
                # initialisation de Configuration
                o_conf = ConfigurationAction("contexte", d_action)
                # on lance l'exécution de run
                o_conf.run()

                # test de l'appel à Configuration.api_create
                o_mock_configuration_api_list.assert_called_once()

                # test de l'appel à Configuration.api_create
                if config_already_exists:
                    o_mock_configuration_api_create.assert_not_called()
                else:
                    o_mock_configuration_api_create.assert_called_once_with(d_action["body_parameters"], route_params={"datastore": None})

                # test api_add_tags
                if "tags" in d_action and d_action["tags"]:
                    o_mock_configuration.api_add_tags.assert_called_once_with(d_action["tags"])
                else:
                    o_mock_configuration.api_add_tags.assert_not_called()

                # test commentaires
                if "comments" in d_action and comments:
                    o_mock_configuration.api_list_comments.assert_called_once_with()
                    self.assertEqual(len(comments), o_mock_configuration.api_add_comment.call_count)
                    for s_comm in comments:
                        o_mock_configuration.api_add_comment.assert_any_call({"text": s_comm})
                else:
                    o_mock_configuration.api_add_comment.assert_not_called()

    def test_run(self) -> None:
        """test de run"""
        # On teste avec et sans configuration renvoyé par api_list
        for b_config_already_exists in [True, False]:
            ## sans tag + sans commentaire
            self.run_args(None, None, b_config_already_exists, False)
            ## tag vide + commentaire vide
            self.run_args({}, [], b_config_already_exists, False)
            ## 1 tag + 1 commentaire
            self.run_args({"tag1": "val1"}, ["comm1"], b_config_already_exists, False)
            ## 2 tag + 4 commentaire
            self.run_args({"tag1": "val1", "tag2": "val2"}, ["comm1", "comm2", "comm3", "comm4"], b_config_already_exists, False)
            ## 2 tag + 4 commentaire + 1 commentaire qui existe déjà
            self.run_args({"tag1": "val1", "tag2": "val2"}, ["comm1", "comm2", "comm3", "comm4"], b_config_already_exists, True)
