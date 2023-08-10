from unittest.mock import patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.Annexes import Annexes
from tests.GpfTestCase import GpfTestCase


class AnnexeTestCase(GpfTestCase):
    """Tests Annexe class.

    cmd : python3 -m unittest -b tests.store.AnnexeTestCase
    """

    def test_publish_by_label(self) -> None:
        "Vérifie le bon fonctionnement de publish_by_label."
        i_file = 10
        l_labels = ["a", "b", "c"]

        for s_datastore in [None, "publish_by_label"]:
            # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
            o_response = GpfTestCase.get_response(text=f"{i_file}")
            with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:

                # on appelle la fonction à tester : publish_by_label
                s_data_recupere = Annexes.publish_by_label(l_labels, s_datastore)

                # on vérifie que route_request est appelé correctement
                o_mock_request.assert_called_once_with(
                    "annexes_publish_by_label",
                    route_params={"datastore": s_datastore},
                    params={"labels": l_labels},
                    method=ApiRequester.POST,
                )
                # on vérifie la similitude des données retournées
                self.assertEqual(i_file, s_data_recupere)

    def test_unpublish_by_label(self) -> None:
        "Vérifie le bon fonctionnement de unpublish_by_label."
        i_file = 10
        l_labels = ["a", "b", "c"]

        for s_datastore in [None, "unpublish_by_label"]:
            # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
            o_response = GpfTestCase.get_response(text=f"{i_file}")
            with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:

                # on appelle la fonction à tester : unpublish_by_label
                s_data_recupere = Annexes.unpublish_by_label(l_labels, s_datastore)

                # on vérifie que route_request est appelé correctement
                o_mock_request.assert_called_once_with(
                    "annexes_unpublish_by_label",
                    route_params={"datastore": s_datastore},
                    params={"labels": l_labels},
                    method=ApiRequester.POST,
                )
                # on vérifie la similitude des données retournées
                self.assertEqual(i_file, s_data_recupere)
