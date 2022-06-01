import unittest
from unittest.mock import patch
import requests
import requests_mock
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.interface.EventInterface import EventInterface


class EventInterfaceTestCase(unittest.TestCase):
    """Tests EventInterface class.

    cmd : python3 -m unittest -b tests.store.EventInterfaceTestCase
    """

    def test_api_list_events(self) -> None:
        "Vérifie le bon fonctionnement de api_list_events."
        l_data = [{"title": "string", "text": "string", "date": "2022-06-01T09:28:09.269Z", "initiator": {"_id": "string", "last_name": "string", "first_name": "string"}}]
        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker() as o_mock:
            o_mock.post("http://test.com/", json=l_data)
            o_response = requests.request("POST", "http://test.com/")
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            # on appelle la fonction à tester :api_list_events
            o_event_interface = EventInterface({"_id": "id_entité"})
            l_data_recupere = o_event_interface.api_events()
            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "store_entity_list_event",
                route_params={"store_entity": "id_entité"},
            )
            # on vérifie la similitude des données retournées
            self.assertEqual(l_data, l_data_recupere)
