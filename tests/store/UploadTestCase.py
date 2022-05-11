import unittest
from unittest.mock import patch

from ignf_gpf_api.store.Upload import Upload
from ignf_gpf_api.io.ApiRequester import ApiRequester


class UploadTestCase(unittest.TestCase):
    """Tests UploadTestCase class.

    cmd : python3 -m unittest -b tests.store.UploadTestCase
    """

    def test_api_push_data_file(self) -> None:
        "Vérifie le bon fonctionnement de api_push_data_file."
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            # On effectue l'ouverture d'une livraison
            # On instancie une livraison à ouvrir
            o_upload_2_open = Upload({"_id": "id_à_ouvrir"})
            # On appelle la fonction api_open
            o_upload_2_open.api_open()
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("upload_open", method=ApiRequester.POST, route_params={"upload": "id_à_ouvrir"})

    def test_api_push_md5_file(self) -> None:
        "Vérifie le bon fonctionnement de api_push_md5_file."

    def test_api_open(self) -> None:
        "Vérifie le bon fonctionnement de api_open."
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            # On effectue l'ouverture d'une livraison
            # On instancie une livraison à ouvrir
            o_upload_2_open = Upload({"_id": "id_à_ouvrir"})
            # On appelle la fonction api_open
            o_upload_2_open.api_open()
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("upload_open", method=ApiRequester.POST, route_params={"upload": "id_à_ouvrir"})

    def test_api_close(self) -> None:
        "Vérifie le bon fonctionnement de api_close."
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            # On effectue la fermeture d'une livraison
            # On instancie une livraison à fermer
            o_upload_2_close = Upload({"_id": "id_à_fermer"})
            # On appelle la fonction api_open
            o_upload_2_close.api_close()
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("upload_close", method=ApiRequester.POST, route_params={"upload": "id_à_fermer"})
