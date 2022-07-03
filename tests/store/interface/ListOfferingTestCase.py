import unittest
from unittest.mock import patch
import requests
import requests_mock

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.Configuration import Configuration
from ignf_gpf_api.store.Offering import Offering


class ListOfferingTestCase(unittest.TestCase):
    """Tests ListOfferingTestCase class.

    cmd : python3 -m unittest -b tests.store.ListOfferingTestCase
    """

    def test_list_offerings(self) -> None:
        """Vérifie le bon fonctionnement de api_list_offerings."""

        l_offerings = {
            "_id": "offering",
            "_entity_title": "offre",
        }

        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker(real_http=True) as o_mock:
            o_mock.post("http://test.com/", json={"_id": "123456789"})
            o_response = requests.request("POST", "http://test.com/")

        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        o_offering = Configuration(l_offerings)

        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            o_offering.api_list_offerings()
            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "configuration_list_sharings",
                route_params={"configuration": "offering"},
                method=ApiRequester.POST,
            )
