import unittest
from unittest.mock import patch
import requests
import requests_mock

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.FullEditInterface import FullEditInterface
from ignf_gpf_api.io.ApiRequester import ApiRequester


class FullEditInterfaceTestCase(unittest.TestCase):
    """Tests FullEditInterface class.

    cmd : python3 -m unittest -b tests.store.FullEditInterfaceTestCase
    """

    def test_api_full_edit(self) -> None:
        "_summary_ : Modifie complètement l'entité sur l'API (PUT)"

        # Infos de l'entité avant la modification complète sur l'API
        d_old_api_data = {
            "_id": "123456789",
            "name": "nom",
            "key": "value",
            "tags": "tag_value",
        }

        # Infos de l'entité après la modification complète sur l'API
        d_full_modified_api_data = {
            "_id": "6598753256",
            "name": "nouveau_nom",
            "key": "new_value",
            "tags": "tag_new_value",
        }

        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker() as o_mock:
            o_mock.post("http://test.com/", json={"_id": "123456789"})
            o_response = requests.request("POST", "http://test.com/")

        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()

        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            o_full_edit_interface = FullEditInterface(d_old_api_data)
            o_full_edit_interface.api_full_edit(d_full_modified_api_data)
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("store_entity_full_edit", data=d_full_modified_api_data, method=ApiRequester.PUT, route_params={"store_entity": "123456789"})
            # Vérification que les infos de l'entité sont maj
            o_store_entity = StoreEntity(d_full_modified_api_data)
            self.assertDictEqual(o_store_entity.get_store_properties(), d_full_modified_api_data)
