import unittest
import requests
import requests_mock
from unittest.mock import patch
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.interface.CommentInterface import CommentInterface


class SharingInterfaceTestCase(unittest.TestCase):
    """Tests SharingInterface class.

    cmd : python3 -m unittest -b tests.store.interface.SharingInterfaceTestCase
    """

    def test_api_add_sharings(self) -> None:
        "Vérifie le bon fonctionnement de api_add_sharings."
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            # On effectue l ajout d'un commentaire
            # On instancie une entité à qui on va ajouter un commentaire
            o_comment_interface = CommentInterface({"_id": "id_entité"})
            # On appelle la fonction api_add_comment
            o_comment_interface.api_add_comment({"text": "comment"})
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_add_comment",
                route_params={"store_entity": "id_entité"},
                data={"text": "comment"},
                method=ApiRequester.POST,
            )

    def test_api_list_sharings(self) -> None:
        "Vérifie le bon fonctionnement de api_list_sharings."
        l_data = [
            {
                "_id": "string",
                "creation": "2022-05-12T07:48:42.123Z",
                "last_modification": "2022-05-12T07:48:42.123Z",
                "text": "string",
                "author": {"_id": "string", "last_name": "string", "first_name": "string"},
            }
        ]
        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker() as o_mock:
            o_mock.post("http://test.com/", json=l_data)
            o_response = requests.request("POST", "http://test.com/")
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            # on appelle la fonction à tester :api_list_comments
            o_comment_interface = CommentInterface({"_id": "id_entité"})
            l_data_recupere = o_comment_interface.api_list_comments()
            # on vérifie que route_request est appelé correctement
            o_mock_request.assert_called_once_with(
                "store_entity_list_comment",
                route_params={"store_entity": "id_entité"},
            )
            # on vérifie la similitude des données retournées
            self.assertEqual(l_data, l_data_recupere)

    def test_api_remove_sharings(self) -> None:
        "Vérifie le bon fonctionnement de api_remove_sharings."
