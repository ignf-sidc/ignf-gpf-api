from unittest.mock import patch
import unittest
import requests
import requests_mock

# from tests.GpfTestCase import GpfTestCase
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
            o_mock.post("http://test.com/", json=d_old_api_data)
            o_response = requests.register_uri("PUT", "http://test.com/", text="resp")

        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()

        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons paramètres
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            o_full_edit_interface = FullEditInterface(d_old_api_data)
            # on fait appel à api_full_edit(d_old_api_data)
            o_full_edit_interface.api_full_edit(d_old_api_data)
            # On appelle la fonction api_update
            o_full_edit_interface.api_update()
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("store_entity_get", route_params={"store_entity": "id_à_maj"})
            # Vérification que les infos de l'entité sont modifiées complètement
            o_store_entity = StoreEntity(d_old_api_data)
            self.assertDictEqual(o_store_entity.get_store_properties(), d_full_modified_api_data)
