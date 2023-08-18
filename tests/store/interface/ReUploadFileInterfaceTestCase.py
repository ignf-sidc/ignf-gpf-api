from pathlib import Path
from unittest.mock import patch
from ignf_gpf_api.io.Config import Config

from ignf_gpf_api.store.interface.ReUploadFileInterface import ReUploadFileInterface
from ignf_gpf_api.io.ApiRequester import ApiRequester

from tests.GpfTestCase import GpfTestCase


class ReUploadFileInterfaceTestCase(GpfTestCase):
    """Tests ReUploadFileInterface class.

    cmd : python3 -m unittest -b tests.store.interface.ReUploadFileInterfaceTestCase
    """

    def test_api_re_upload(self) -> None:
        """Modifie complètement l'entité sur l'API (PUT)"""

        # Infos de l'entité avant la modification complète sur l'API
        p_file = Path("rep/file2")
        s_file_key = "file"
        o_full_edit_interface = ReUploadFileInterface({"_id": "123456789"})

        with patch.object(ApiRequester, "route_upload_file", return_value=None) as o_mock_request:
            with patch.object(o_full_edit_interface, "api_update", return_value=None) as o_mock_update:
                with patch.object(Config, "get_str", return_value=s_file_key):

                    # On appelle la fonction api_re_upload
                    o_full_edit_interface.api_re_upload(p_file)

                    # Vérification sur o_mock_request
                    o_mock_request.assert_called_once_with(
                        "store_entity_re_upload",
                        p_file,
                        s_file_key,
                        method=ApiRequester.PUT,
                    )
                    o_mock_update.assert_called_once_with()
