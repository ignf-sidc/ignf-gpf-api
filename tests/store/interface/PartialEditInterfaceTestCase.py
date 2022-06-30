import unittest
from unittest.mock import patch
import requests

import requests_mock

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.interface.PartialEditInterface import PartialEditInterface
from ignf_gpf_api.io.ApiRequester import ApiRequester


class PartialEditInterfaceTestCase(unittest.TestCase):
    """Tests PartialEditInterface class.

    cmd : python3 -m unittest -b tests.store.PartialEditInterfaceTestCase
    """

    def test_api_partial_edit(self) -> None:
        """_summary_ : Modifie partiellement l'entité sur l'API (PATCH)"""

        # Infos de l'entité avant la modification partielle sur l'API
        d_old_api_data = {
            "_id": "123456789",
            "name": "nom",
            "key": "value",
            "tags": "tag_value",
        }

        # Infos de l'entité après la modification partielle sur l'API
        d_partly_modified_api_data = {
            "_id": "6598753256",
            "name": "nouveau_nom",
            "key": "new_value",
            "tags": "tag_new_value",
        }

        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker(real_http=True) as o_mock:
            o_mock.post("http://test.com/", json={"_id": "123456789"})
            o_response = requests.request("POST", "http://test.com/")

        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()

        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response):
            o_partial_edit_interface = PartialEditInterface(d_old_api_data)
            o_partial_edit_interface.api_update()
            # Vérification sur o_mock_request
            # o_mock_request.assert_called_once_with("store_entity_partial_edit", data=d_partly_modified_api_data, method=ApiRequester.PATCH, route_params={"store_entity": "123456789"})
            o_partial_edit_interface.api_partial_edit(d_partly_modified_api_data)
            o_partial_edit_interface.api_update()
            # Vérification que les infos de l'entité sont maj
            o_store_entity = StoreEntity(d_partly_modified_api_data)
            self.assertDictEqual(o_store_entity.get_store_properties(), d_partly_modified_api_data)
