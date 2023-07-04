from unittest.mock import patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.Endpoint import Endpoint

from tests.GpfTestCase import GpfTestCase


class EndpointTestCase(GpfTestCase):
    """Tests Endpoint class.

    cmd : python3 -m unittest -b tests.store.EndpointTestCase
    """

    def test_api_list(self) -> None:
        """Vérifie le bon fonctionnement de api_list."""
        # Extrait de la requête "datastore" de l'API
        d_data = {
            "endpoints": [
                {
                    "endpoint": {
                        "_id": "endpoint_1",
                        "name": "Service WMTS",
                        "type": "WMTS-TMS",
                    }
                },
                {
                    "endpoint": {
                        "_id": "endpoint_2",
                        "name": "Service de téléchargement",
                        "type": "DOWNLOAD",
                    }
                },
            ]
        }

        # Instanciation d'une fausse réponse HTTP
        o_response = GpfTestCase.get_response(json=d_data)

        # 1 : pas de filtres
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester(), "route_request", return_value=o_response) as o_mock_request:
            l_endpoints = Endpoint.api_list()
            # on vérifie que route_request est appelée correctement
            o_mock_request.assert_called_once_with("datastore_get")
            # on vérifie qu'on a bien récupéré une liste de 2 Endpoints
            self.assertIsInstance(l_endpoints, list)
            self.assertEqual(len(l_endpoints), 2)
            self.assertIsInstance(l_endpoints[0], Endpoint)
            self.assertIsInstance(l_endpoints[1], Endpoint)
            self.assertEqual(l_endpoints[0].id, "endpoint_1")
            self.assertEqual(l_endpoints[1].id, "endpoint_2")

        # 2 : filtre sur le nom
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester(), "route_request", return_value=o_response) as o_mock_request:
            l_endpoints = Endpoint.api_list(infos_filter={"name": "Service WMTS"})
            # on vérifie que route_request est appelée correctement
            o_mock_request.assert_called_once_with("datastore_get")
            # on vérifie qu'on a bien récupéré une liste de 1 Endpoint
            self.assertIsInstance(l_endpoints, list)
            self.assertEqual(len(l_endpoints), 1)
            self.assertIsInstance(l_endpoints[0], Endpoint)
            self.assertEqual(l_endpoints[0].id, "endpoint_1")

        # 2 : filtre sur le type
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester(), "route_request", return_value=o_response) as o_mock_request:
            l_endpoints = Endpoint.api_list(infos_filter={"type": "DOWNLOAD"})
            # on vérifie que route_request est appelée correctement
            o_mock_request.assert_called_once_with("datastore_get")
            # on vérifie qu'on a bien récupéré une liste de 1 Endpoint
            self.assertIsInstance(l_endpoints, list)
            self.assertEqual(len(l_endpoints), 1)
            self.assertIsInstance(l_endpoints[0], Endpoint)
            self.assertEqual(l_endpoints[0].id, "endpoint_2")
