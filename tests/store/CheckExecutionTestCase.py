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
        l_rep = [
            {"datastore": "datastore_id", "data": s_data, "rep": s_data},
            {"datastore": "datastore_id", "data": "", "rep": ""},
            {"datastore": "datastore_id", "data": "[]", "rep": ""},
            {"datastore": "datastore_id", "data": '["log1", "log2", " log \\"complexe\\""]', "rep": 'log1\nlog2\n log "complexe"'},
        ]

        for d_rep in l_rep:
            o_response = GpfTestCase.get_response(text=d_rep["data"])
            # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
            with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:
                # on appelle la fonction à tester : api_logs
                o_check_execution = CheckExecution({"_id": "id_entité"}, datastore=d_rep["datastore"])
                s_data_recupere = o_check_execution.api_logs()
                # on vérifie que route_request est appelé correctement
                o_mock_request.assert_called_once_with(
                    "check_execution_logs",
                    route_params={"datastore": d_rep["datastore"], "check_execution": "id_entité"},
                )
                # on vérifie la similitude des données retournées
                self.assertEqual(d_rep["rep"], s_data_recupere)
