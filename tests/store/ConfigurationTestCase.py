import unittest
from unittest.mock import patch
import requests
import requests_mock

from ignf_gpf_api.store.Offering import Offering
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.Configuration import Configuration


class ConfigurationTestCase(unittest.TestCase):
    """Tests ListOfferingTestCase class.

    cmd : python3 -m unittest -b tests.store.ConfigurationTestCase
    """

    def test_list_offerings(self) -> None:
        """Vérifie le bon fonctionnement de api_list_offerings."""

        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker(real_http=True) as o_mock:
            o_mock.post("http://test.com/", json=[{"_id": "offering_1"}, {"_id": "offering_2"}])
            o_response = requests.request("POST", "http://test.com/")

        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        o_offering = Configuration({"_id": "123456789"})

        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            l_offerings = o_offering.api_list_offerings()
            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "configuration_list_offerings",
                route_params={"configuration": "123456789"},
                method=ApiRequester.GET,
            )
            # on vérifie qu'on a bien récupéré une liste d'Offering
            self.assertIsInstance(l_offerings, list)
            self.assertIsInstance(l_offerings[0], Offering)
            self.assertIsInstance(l_offerings[1], Offering)
            self.assertEqual(l_offerings[0].id, "offering_1")
            self.assertEqual(l_offerings[1].id, "offering_2")
