from unittest.mock import patch, mock_open
from pathlib import Path
from typing import Any, Dict, List

from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.Upload import Upload
from ignf_gpf_api.io.ApiRequester import ApiRequester
from tests.GpfTestCase import GpfTestCase


class UploadTestCase(GpfTestCase):
    """Tests Upload class.

    cmd : python3 -m unittest -b tests.store.UploadTestCase
    """

    def test_api_push_data_file(self) -> None:
        "Vérifie le bon fonctionnement de api_push_data_file."
        # On instancie une livraison pour laquelle on veut pousser des fichiers
        o_upload = Upload({"_id": "id_de_test"})
        # On récupère le nom de la clé associée au fichier
        s_key_file = Config().get("upload_creation", "push_data_file_key")
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            o_opener = mock_open()
            # on va mocker le { file_path.open("rb") } présent dans la fct api_push_data_file :
            with patch.object(Path, "open", return_value=o_opener.return_value) as o_mock_open:
                # Initialisation des paramètres utilisés par la fonction à tester
                p_file_path = Path("path/dun/fichier/a/tester.txt")
                # on prend un chemin coté api
                s_api_path = "path/cote/api"
                # On appelle la fonction que l'on veut tester
                o_upload.api_push_data_file(p_file_path, s_api_path)

                # Vérification sur o_mock_request
                o_mock_request.assert_called_once_with(
                    "upload_push_data",
                    method=ApiRequester.POST,
                    route_params={"upload": "id_de_test"},
                    params={"path": s_api_path},
                    files={s_key_file: (p_file_path.name, o_opener.return_value)},
                )
                # Vérification sur o_mock_open (lecture binary)
                o_mock_open.assert_called_once_with("rb")

    def test_api_push_md5_file(self) -> None:
        "Vérifie le bon fonctionnement de api_push_md5_file."
        # On instancie une livraison pour laquelle on veut pousser des fichiers
        o_upload = Upload({"_id": "id_de_test"})
        # On récupère le nom de la clé associée au fichier
        s_key_file = Config().get("upload_creation", "push_md5_file_key")
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            o_opener = mock_open()
            with patch.object(Path, "open", return_value=o_opener.return_value) as o_mock_open:
                # Initialisation des paramètres utilisés par la fonction à tester
                p_file_path = Path("path/dun/fichier/a/tester.txt")
                # On appelle la fonction que l'on veut tester
                o_upload.api_push_md5_file(p_file_path)

                # Vérification sur o_mock_request
                o_mock_request.assert_called_once_with(
                    "upload_push_md5",
                    method=ApiRequester.POST,
                    route_params={"upload": "id_de_test"},
                    files={s_key_file: (p_file_path.name, o_opener.return_value)},
                )
                # Vérification sur o_mock_open (lecture binary)
                o_mock_open.assert_called_once_with("rb")

    def test_api_delete_data_file_1(self) -> None:
        "Vérifie le bon fonctionnement de api_delete_data_file si le chemin ne contient pas data/."
        # On instancie une livraison pour laquelle on veut supprimer des fichiers
        # peu importe si la livraison comporte ou pas des fichiers
        o_upload = Upload({"_id": "id_de_test"})
        # on prend un chemin coté api
        s_api_path = "path/cote/api"

        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On appelle la fonction que l'on veut tester
            o_upload.api_delete_data_file(s_api_path)

            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "upload_delete_data",
                method=ApiRequester.DELETE,
                route_params={"upload": "id_de_test"},
                params={"path": s_api_path},
            )

    def test_api_delete_data_file_2(self) -> None:
        "Vérifie le bon fonctionnement de api_delete_data_file si le chemin contient data/."
        # On instancie une livraison pour laquelle on veut supprimer des fichiers
        # peu importe si la livraison comporte ou pas des fichiers
        o_upload = Upload({"_id": "id_de_test"})
        # on prend un chemin coté api
        s_api_path = "data/path/cote/api"

        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On appelle la fonction que l'on veut tester
            o_upload.api_delete_data_file(s_api_path)

            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "upload_delete_data",
                method=ApiRequester.DELETE,
                route_params={"upload": "id_de_test"},
                params={"path": s_api_path[5:]},  # le data/ a dû être retiré
            )

    def test_api_delete_md5_file(self) -> None:
        "Vérifie le bon fonctionnement de api_delete_md5_file."
        # On instancie une livraison pour laquelle on veut supprimer des fichiers md5
        # peu importe si la livraison comporte ou pas des fichiers
        o_upload = Upload({"_id": "id_de_test"})
        # on prend un chemin coté api
        s_api_path = "path/cote/api"

        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On appelle la fonction que l'on veut tester
            o_upload.api_delete_md5_file(s_api_path)

            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "upload_delete_md5",
                method=ApiRequester.DELETE,
                route_params={"upload": "id_de_test"},
                params={"path": s_api_path},
            )

    def test_api_open(self) -> None:
        "Vérifie le bon fonctionnement de api_open."
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On effectue l'ouverture d'une livraison
            # On instancie une livraison à ouvrir
            o_upload_2_open = Upload({"_id": "id_à_ouvrir"})
            # On mock la fonction api_update
            with patch.object(o_upload_2_open, "api_update", return_value=None) as o_mock_api_update:
                # On appelle la fonction api_open
                o_upload_2_open.api_open()
                # Vérification sur o_mock_request
                o_mock_request.assert_called_once_with("upload_open", method=ApiRequester.POST, route_params={"upload": "id_à_ouvrir"})
                # Vérification de l'appel à api_update
                o_mock_api_update.assert_called_once()

    def test_api_close(self) -> None:
        "Vérifie le bon fonctionnement de api_close."
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On effectue la fermeture d'une livraison
            # On instancie une livraison à fermer
            o_upload_2_close = Upload({"_id": "id_à_fermer"})
            # On mock la fonction api_update
            with patch.object(o_upload_2_close, "api_update", return_value=None) as o_mock_api_update:
                # On appelle la fonction api_close
                o_upload_2_close.api_close()
                # Vérification sur o_mock_request
                o_mock_request.assert_called_once_with("upload_close", method=ApiRequester.POST, route_params={"upload": "id_à_fermer"})
                # Vérification de l'appel à api_update
                o_mock_api_update.assert_called_once()

    def test_api_tree(self) -> None:
        "Vérifie le bon fonctionnement de api_tree."
        l_tree_wanted = [{"key_1": "value_1", "key_2": "value_2"}]
        # Instanciation d'une fausse réponse HTTP
        o_response = GpfTestCase.get_response(json=l_tree_wanted)
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:
            # On instancie un upload
            o_upload = Upload({"_id": "identifiant"})
            # On appelle api_tree
            l_tree = o_upload.api_tree()
            # Vérification sur o_mock_request (route upload_tree avec comme params de route l'id)
            o_mock_request.assert_called_once_with("upload_tree", route_params={"upload": "identifiant"})
            # Vérifications sur l_tree
            self.assertEqual(l_tree, l_tree_wanted)

    def test_api_list_checks(self) -> None:
        "Vérifie le bon fonctionnement de api_list_checks."
        d_list_checks_wanted: Dict[str, List[Dict[str, Any]]] = {"key_1": [], "key_2": []}
        # Instanciation d'une fausse réponse HTTP
        o_response = GpfTestCase.get_response(json=d_list_checks_wanted)
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:
            # On instancie un upload
            o_upload = Upload({"_id": "identifiant"})
            # On appelle api_list_checks
            d_list_checks = o_upload.api_list_checks()
            # Vérification sur o_mock_request (route api_list_checks avec comme params de route l'id)
            o_mock_request.assert_called_once_with("upload_list_checks", route_params={"upload": "identifiant"})
            # Vérifications sur list_checks
            self.assertEqual(d_list_checks, d_list_checks_wanted)

    def test_api_run_checks(self) -> None:
        "Vérifie le bon fonctionnement de api_run_checks."
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons params
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On instancie une livraison
            o_upload_run_checks = Upload({"_id": "id"})
            # liste des ids à verifier
            l_list_checks_ids: List[Any] = ["id1", "id2"]
            # On appelle la fonction api_run_checks
            o_upload_run_checks.api_run_checks(l_list_checks_ids)
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("upload_run_checks", method=ApiRequester.POST, route_params={"upload": "id"}, data=["id1", "id2"])
