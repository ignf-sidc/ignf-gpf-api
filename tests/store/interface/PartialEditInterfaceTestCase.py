from unittest.mock import patch

from ignf_gpf_api.store.interface.PartialEditInterface import PartialEditInterface
from ignf_gpf_api.io.ApiRequester import ApiRequester

from tests.GpfTestCase import GpfTestCase


class PartialEditInterfaceTestCase(GpfTestCase):
    """Tests PartialEditInterface class.
    cmd : python3 -m unittest -b tests.store.interface.PartialEditInterfaceTestCase
    """

    def test_api_partial_edit(self) -> None:
        """Modifie partiellement l'entité sur l'API (PUT)"""

        # Infos de l'entité avant la modification complète sur l'API
        d_old_api_data = {
            "_id": "123456789",
            "name": "nom",
            "key": "value",
            "tags": "tag_value",
        }

        # Infos de l'entité après la modification complète sur l'API
        d_partly_modified_api_data = {
            "_id": "123456789",
            "name": "new_nom",
            "key": "new_value",
            "tags": "new_tag_value",
        }

        o_partial_edit_interface = PartialEditInterface(d_old_api_data)

        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request, patch.object(o_partial_edit_interface, "api_update", return_value=None) as o_mock_update:
            # On appelle la fonction api_partial_edit
            o_partial_edit_interface.api_partial_edit(d_partly_modified_api_data)
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_partial_edit",
                route_params={"store_entity": "123456789"},
                method=ApiRequester.PATCH,
                data=d_partly_modified_api_data,
            )
            o_mock_update.assert_called_once_with()
