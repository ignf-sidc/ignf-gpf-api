import unittest
from unittest.mock import patch, mock_open
from pathlib import Path

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
        # On instancie une livraison pour laquelle on veut pousser des fichiers
        o_upload_2_push_data = Upload({"_id": "id_fichier_à_pousser"})
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            o_opener = mock_open()
            with patch.object(Path, "open", return_value=o_opener.return_value) as o_mock_open:
                # Initialisation des paramètres utilisés par la fonction à tester
                o_file_path = Path("path/dun/fichier/a/tester.txt")
                s_api_path = "path/cote/api"
                # On appelle la fonction api_push_data
                o_upload_2_push_data.api_push_data_file(o_file_path, s_api_path)

                # Vérification sur o_mock_request
                o_mock_request.assert_called_once_with(
                    "upload_push_data",
                    method=ApiRequester.POST,
                    route_params={"upload": "id_fichier_à_pousser"},
                    params={"path": s_api_path},
                    files={"file": (o_file_path.name, o_opener.return_value)},
                )
                # Vérification sur o_mock_open
                o_mock_open.assert_called_once_with("rb")

    def test_api_push_md5_file(self) -> None:
        "Vérifie le bon fonctionnement de api_push_md5_file."
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On instancie une livraison pour laquelle on veut pousser des fichiers
        o_upload_2_push_md5 = Upload({"_id": "id_md5"})
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            o_opener = mock_open()
            with patch.object(Path, "open", return_value=o_opener.return_value) as o_mock_open:
                # Initialisation des paramètres utilisés par la fonction à tester
                o_file_path = Path("path/dun/fichier/a/tester.txt")
                # On appelle la fonction api_push_data
                o_upload_2_push_md5.api_push_md5_file(o_file_path)

                # Vérification sur o_mock_request
                o_mock_request.assert_called_once_with(
                    "upload_push_md5",
                    method=ApiRequester.POST,
                    route_params={"upload": "id_md5"},
                    files={"file": (o_file_path.name, o_opener.return_value)},
                )
                # Vérification sur o_mock_open
                o_mock_open.assert_called_once_with("rb")

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
