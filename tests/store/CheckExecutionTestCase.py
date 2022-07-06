from unittest.mock import patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.CheckExecution import CheckExecution
from tests.GpfTestCase import GpfTestCase


class CheckExecutionTestCase(GpfTestCase):
    """Tests CheckExecution class.

    cmd : python3 -m unittest -b tests.store.CheckExecutionTestCase
    """

    def test_api_logs(self) -> None:
        "Vérifie le bon fonctionnement de api_logs."
        s_data = "2022/05/18 14:29:25       INFO §USER§ Envoi du signal de début de l'exécution à l'API.\n2022/05/18 14:29:25       INFO §USER§ Signal transmis avec succès."
        o_response = GpfTestCase.get_response(text=s_data)
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:
            # on appelle la fonction à tester : api_logs
            o_check_execution = CheckExecution({"_id": "id_entité"})
            s_data_recupere = o_check_execution.api_logs()
            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "check_execution_logs",
                route_params={"check_execution": "id_entité"},
            )
            # on vérifie la similitude des données retournées
            self.assertEqual(s_data, s_data_recupere)
