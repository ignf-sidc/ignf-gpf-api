from unittest.mock import patch

from ignf_gpf_api.store.interface.FullEditInterface import FullEditInterface
from ignf_gpf_api.io.ApiRequester import ApiRequester

from tests.GpfTestCase import GpfTestCase


class FullEditInterfaceTestCase(GpfTestCase):
    """Tests FullEditInterface class.

    cmd : python3 -m unittest -b tests.store.interface.FullEditInterfaceTestCase
    """

    def test_api_full_edit(self) -> None:
        """Modifie complètement l'entité sur l'API (PUT)"""

        # Infos de l'entité avant la modification complète sur l'API
        d_old_api_data = {
            "_id": "123456789",
            "name": "nom",
            "key": "value",
            "tags": "tag_value",
        }

        # Infos de l'entité après la modification complète sur l'API
        d_full_modified_api_data = {
            "_id": "123456789",
            "name": "new_nom",
            "key": "new_value",
            "tags": "new_tag_value",
        }

        o_full_edit_interface = FullEditInterface(d_old_api_data)

        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request, patch.object(o_full_edit_interface, "api_update", return_value=None) as o_mock_update:
            # On appelle la fonction api_full_edit
            o_full_edit_interface.api_full_edit(d_full_modified_api_data)
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_full_edit",
                route_params={"store_entity": "123456789"},
                method=ApiRequester.PUT,
                data=d_full_modified_api_data,
            )
            o_mock_update.assert_called_once_with()
