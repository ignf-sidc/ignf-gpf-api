import unittest
from unittest.mock import patch
import requests
import requests_mock
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.ProcessingExecution import ProcessingExecution


class ProcessingExecutionTestCase(unittest.TestCase):
    """Tests ProcessingExecution class.

    cmd : python3 -m unittest -b tests.store.ProcessingExecutionTestCase
    """

    def test_api_logs(self) -> None:
        "Vérifie le bon fonctionnement de api_logs."
        s_data = "2022/05/18 14:29:25       INFO §USER§ Envoi du signal de début de l'exécution à l'API.\n2022/05/18 14:29:25       INFO §USER§ Signal transmis avec succès."
        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker() as o_mock:
            o_mock.get("http://test.com/", text=s_data)
            o_response = requests.request("get", "http://test.com/")
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            # on appelle la fonction à tester : api_logs
            o_processing_execution = ProcessingExecution({"_id": "id_entité"})
            s_data_recupere = o_processing_execution.api_logs()

            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "processing_execution_logs",
                route_params={"processing_execution": "id_entité"},
            )
            # on vérifie la similitude des données retournées
            self.assertEqual(s_data, s_data_recupere)

    def test_api_launch(self) -> None:
        "Vérifie le bon fonctionnement de api_launch."
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            # on appelle la fonction à tester : api_launch
            o_processing_execution = ProcessingExecution({"_id": "id_entité"})
            o_processing_execution.api_launch()

            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "processing_execution_launch",
                route_params={"processing_execution": "id_entité"},
                method=ApiRequester.POST,
            )

    def test_api_abort(self) -> None:
        "Vérifie le bon fonctionnement de api_abort."
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            # on appelle la fonction à tester : api_abort
            o_processing_execution = ProcessingExecution({"_id": "id_entité"})
            o_processing_execution.api_abort()

            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "processing_execution_abort",
                route_params={"processing_execution": "id_entité"},
                method=ApiRequester.POST,
            )
