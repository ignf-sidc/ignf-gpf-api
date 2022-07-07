from unittest.mock import patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.interface.SharingInterface import SharingInterface
from tests.GpfTestCase import GpfTestCase


class SharingInterfaceTestCase(GpfTestCase):
    """Tests SharingInterface class.

    cmd : python3 -m unittest -b tests.store.interface.SharingInterfaceTestCase
    """

    def test_api_add_sharings(self) -> None:
        "Vérifie le bon fonctionnement de api_add_sharings."
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On effectue l ajout d'un commentaire
            # On instancie une entité à qui on va ajouter un commentaire
            o_sharing_interface = SharingInterface({"_id": "id_entité"})
            # On appelle la fonction api_add_sharings
            o_sharing_interface.api_add_sharings(["_id"])
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_add_sharings",
                route_params={"store_entity": "id_entité"},
                data=["_id"],
                method=ApiRequester.POST,
            )

    def test_api_list_sharings(self) -> None:
        "Vérifie le bon fonctionnement de api_list_sharings."
        l_data = [
            {
                "_id": "string",
                "creation": "2022-06-01T08:24:26.754Z",
                "last_modification": "2022-06-01T10:00:00.754Z",
                "text": "string",
                "initiator": {"_id": "string", "last_name": "string", "first_name": "string"},
            }
        ]
        # Instanciation d'une fausse réponse HTTP
        o_response = GpfTestCase.get_response(json=l_data)
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:
            # on appelle la fonction à tester :api_list_sharings
            o_sharing_interface = SharingInterface({"_id": "id_entité"})
            l_data_recupere = o_sharing_interface.api_list_sharings()
            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "store_entity_list_sharings",
                route_params={"store_entity": "id_entité"},
            )
            # on vérifie la similitude des données retournées
            self.assertEqual(l_data, l_data_recupere)

    def test_api_remove_sharings(self) -> None:
        "Vérifie le bon fonctionnement de api_remove_sharings."
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On effectue la suppression d'un commentaire
            # On instancie une entité dont on va supprimer le partage de livraison
            o_sharing_interface = SharingInterface({"_id": "id_entité"})
            # On appelle la fonction api_remove_sharing
            o_sharing_interface.api_remove_sharings(["_id"])
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_remove_sharings",
                route_params={"store_entity": "id_entité"},
                params={"datastores[]": ["_id"]},
                method=ApiRequester.DELETE,
            )
