from pathlib import Path
import unittest
from unittest.mock import patch
from http import HTTPStatus
import requests_mock

from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.auth.Authentifier import Authentifier
from ignf_gpf_api.auth.Errors import AuthentificationError

# pylint:disable=protected-access


class AuthentifierTestCase(unittest.TestCase):
    """Tests ConfigTestCase class.

    cmd : python3 -m unittest -b tests.auth.AuthentifierTestCase
    """

    config_path = Path(__file__).parent.parent / "_config"
    url = "https://store_authentification.test.io/auth/realms/master/protocol/openid-connect/token"
    valid_token = {
        "access_token": "test_token",
        "expires_in": 300,
    }

    @classmethod
    def setUpClass(cls) -> None:
        # On détruit le Singleton Config
        Config._instance = None
        # On charge une config spéciale pour les tests d'authentification
        cConfig = Config()
        cConfig.read(AuthentifierTestCase.config_path / "config_test_authentifier.ini")

    def setUp(self) -> None:
        # On détruit le singleton Authentifier
        Authentifier._instance = None

    @classmethod
    def tearDownClass(cls) -> None:
        # On détruit le Singleton Config
        Config._instance = None

    def test_get_access_token_string_ok(self) -> None:
        """Vérifie le bon fonctionnement de get_access_token_string dans un cas normal."""
        # On mock...
        with requests_mock.Mocker() as cMock:
            # Une authentification réussie
            cMock.post(AuthentifierTestCase.url, json=AuthentifierTestCase.valid_token)
            # On tente de récupérer un token...
            sToken = Authentifier().get_access_token_string()
            # Il doit être ok
            self.assertEqual(sToken, "test_token")
            # On a dû faire une requête
            self.assertEqual(cMock.call_count, 1, "cMock.call_count == 1")
            # Vérifications sur l'historique (enfin ici y'a une requête...)
            cHistory = cMock.request_history
            # Requête 1 : vérification du type
            self.assertEqual(cHistory[0].method.lower(), "post", "method == post")
            # Requête 1 : vérification du text
            sText = "grant_type=password&username=TEST_LOGIN&password=TEST_PASSWORD&client_id=TEST_CLIENT_ID"
            self.assertEqual(cHistory[0].text, sText, "check text")

    def test_get_access_token_string_2_attempts(self) -> None:
        """Vérifie le bon fonctionnement de get_access_token_string si plusieurs tentatives."""
        # On mock...
        with requests_mock.Mocker() as cMock:
            # Deux erreurs puis une authentification réussie
            cMock.post(
                AuthentifierTestCase.url,
                [
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"json": AuthentifierTestCase.valid_token},
                ],
            )
            # On tente de récupérer un token...
            sToken = Authentifier().get_access_token_string()
            # Il doit être ok
            self.assertEqual(sToken, "test_token")
            # On a dû faire 3 requêtes
            self.assertEqual(cMock.call_count, 3, "cMock.call_count == 3")

    def test_get_access_token_string_too_much_attempts(self) -> None:
        """Vérifie le bon fonctionnement de get_access_token_string si trop de tentatives."""
        # On mock...
        with requests_mock.Mocker() as cMock:
            # Trop d'erreurs
            cMock.post(
                AuthentifierTestCase.url,
                [
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                ],
            )
            # On s'attend à une exception
            with self.assertRaises(AuthentificationError) as cArc:
                # On tente de récupérer un token...
                Authentifier().get_access_token_string()
            # On doit avoir un message d'erreur
            self.assertEqual(cArc.exception.message, "La récupération du jeton d'authentification a échoué après 3 tentatives")
            # On a dû faire 4 requêtes
            self.assertEqual(cMock.call_count, 4, "cMock.call_count == 4")

    def test_get_http_header(self) -> None:
        """Vérifie le bon fonctionnement de test_get_http_header."""
        # On mock get_access_token_string qui est déjà testée
        with patch.object(Authentifier, "get_access_token_string", return_value="test_token") as c_mock_method:
            d_http_header_default = Authentifier().get_http_header()
            d_http_header_false = Authentifier().get_http_header(json_content_type=False)
            d_http_header_true = Authentifier().get_http_header(json_content_type=True)

        # Vérifications dictionnaire
        # Les 3 dict ont la bonne valeur pour la clé "Authorization"
        self.assertEqual(d_http_header_default["Authorization"], "Bearer test_token")
        self.assertEqual(d_http_header_false["Authorization"], "Bearer test_token")
        self.assertEqual(d_http_header_true["Authorization"], "Bearer test_token")
        # Les 2 dict default et false n'ont qu'une seule clé
        self.assertEqual(len(d_http_header_default.keys()), 1, "len(d_http_header_default) == 1")
        self.assertEqual(len(d_http_header_false.keys()), 1, "len(d_http_header_false) == 1")
        # Le dict true a 2 clés
        self.assertEqual(len(d_http_header_true.keys()), 2, "len(d_http_header_true) == 2")
        # La clé "" vaut ""
        self.assertEqual(d_http_header_true["content-type"], "application/json")

        # Vérifications c_mock_method
        # La fonction a été appelée
        self.assertTrue(c_mock_method.called)
        # Et ce 3 fois
        self.assertEqual(c_mock_method.call_count, 3)
