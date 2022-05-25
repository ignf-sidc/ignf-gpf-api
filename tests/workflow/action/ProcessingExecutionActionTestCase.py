from typing import Any, Dict, List, Optional

import unittest
from unittest.mock import patch, MagicMock

from ignf_gpf_api.store.ProcessingExecution import ProcessingExecution
from ignf_gpf_api.store.StoredData import StoredData
from ignf_gpf_api.store.Upload import Upload
from ignf_gpf_api.workflow.action.ProcessingExecutionAction import ProcessingExecutionAction


class ProcessingExecutionActionTestCase(unittest.TestCase):
    """Tests UploadAction class.

    cmd : python3 -m unittest -b tests.workflow.action.ProcessingExecutionActionTestCase
    """

    def run_args(self, tags: Optional[Dict[str, Any]], comments: Optional[List],  s_type_output: str) -> None:
        """lancement de ProcessingExecutionAction.run selon param

        Args:
            tags (Optional[Dict[str, Any]]): dict des tags ou None
            comments (Optional[List]): list des comments ou None
            s_type_output (str): type de l'output (stored_data ou upload)
        """
        d_action = {"type": "processing-execution", "parameters": {"param": "valeur"}}
        if tags is not None:
            d_action["tags"] = tags
        if comments is not None:
            d_action["comments"] = comments

        # initialisation de ProcessingExecutionAction
        o_pea = ProcessingExecutionAction("contexte", d_action)

        # mock de processing execution
        d_store_properties = {"output": {s_type_output: {"_id": "id"}}}
        o_mock_precession = MagicMock()
        o_mock_precession.get_store_properties.return_value = d_store_properties
        o_mock_precession.api_launch.return_value = None

        # mock de upload
        o_mock_upload = MagicMock()
        o_mock_upload.api_add_tags.return_value = None
        o_mock_upload.api_add_comment.return_value = None

        # mock de stored_data
        o_mock_stored_data = MagicMock()
        o_mock_stored_data.api_add_tags.return_value = None
        o_mock_stored_data.api_add_comment.return_value = None

        # suppression de la mise en page forcé pour le with
        # fmt: off
        with patch.object(Upload, "api_get", return_value=o_mock_upload) as o_mock_processing_upload_api_get, \
            patch.object(StoredData, "api_get", return_value=o_mock_stored_data) as o_mock_processing_store_data_api_get, \
            patch.object(ProcessingExecution, "api_create", return_value=o_mock_precession) as o_mock_processing_execution_api_create \
        :
            # fmt: on
            # on lance l'exécution de run
            o_pea.run()

            # test de l'appel à ProcessingExecution.api_create
            o_mock_processing_execution_api_create.assert_called_once_with(d_action['parameters'])
            # un appel à ProcessingExecution().get_store_properties
            o_mock_precession.get_store_properties.assert_called_once_with()

            # verif appel à Upload/StoredData
            if "stored_data" in d_store_properties["output"]:
                # test  .api_get
                o_mock_processing_store_data_api_get.assert_called_once_with("id")
                o_mock_processing_upload_api_get.assert_not_called()

                # test api_add_tags
                if "tags" in d_action and d_action["tags"]:
                    o_mock_stored_data.api_add_tags.assert_called_once_with(d_action["tags"])
                else:
                    o_mock_stored_data.api_add_tags.assert_not_called()
                o_mock_upload.api_add_tags.assert_not_called()

                # test commentaires
                if "comments" in d_action and d_action["comments"]:
                    self.assertEqual(len(d_action["comments"]), o_mock_stored_data.api_add_comment.call_count)
                    for s_comm in d_action["comments"]:
                        o_mock_stored_data.api_add_comment.assert_any_call({"text": s_comm})
                else:
                    o_mock_stored_data.api_add_comment.assert_not_called()
                o_mock_upload.api_add_comment.assert_not_called()


            elif "upload" in  d_store_properties["output"]:
                # test  .api_get
                o_mock_processing_upload_api_get.assert_called_once_with("id")
                o_mock_processing_store_data_api_get.assert_not_called()

                # test api_add_tags
                if "tags" in d_action and d_action["tags"]:
                    o_mock_upload.api_add_tags.assert_called_once_with(d_action["tags"])
                else:
                    o_mock_upload.api_add_tags.assert_not_called()
                o_mock_stored_data.api_add_tags.assert_not_called()

                # test commentaires
                if "comments" in d_action and d_action["comments"]:
                    self.assertEqual(len(d_action["comments"]), o_mock_upload.api_add_comment.call_count)
                    for s_comm in d_action["comments"]:
                        o_mock_upload.api_add_comment.assert_any_call({"text": s_comm})
                else:
                    o_mock_upload.api_add_comment.assert_not_called()
                o_mock_stored_data.api_add_comment.assert_not_called()

            # un appel à api_launch
            o_mock_precession.api_launch.assert_called_once_with()

    def test_run(self) -> None:
        """test de run"""
        # test upload
        for s_type_output in [ "upload", "stored_data"]:
            ## sans tag + sans commentaire
            self.run_args(None, None, s_type_output)
            ## tag vide + commentaire vide
            self.run_args({}, [], s_type_output)
            ## 1 tag + 1 commentaire
            self.run_args({"tag1": "val1"}, ["comm1"], s_type_output)
            ## 2 tag + 4 commentaire
            self.run_args({"tag1": "val1", "tag2": "val2"}, ["comm1", "comm2", "comm3", "comm4"], s_type_output)
