from unittest.mock import patch
from http import HTTPStatus
import requests_mock

from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.auth.Authentifier import Authentifier
from ignf_gpf_api.auth.Errors import AuthentificationError
from tests.GpfTestCase import GpfTestCase

# pylint:disable=protected-access


class AuthentifierTestCase(GpfTestCase):
    """Tests Authentifier class.

    cmd : python3 -m unittest -b tests.auth.AuthentifierTestCase
    """

    url = "https://store_authentification.test.io/auth/realms/master/protocol/openid-connect/token"
    valid_token = {
        "access_token": "test_token",
        "expires_in": 300,
    }

    @classmethod
    def setUpClass(cls) -> None:
        """fonction lancée une fois avant tous les tests de la classe"""
        super().setUpClass()
        # On détruit le Singleton Config
        Config._instance = None
        # On charge une config spéciale pour les tests d'authentification
        o_config = Config()
        o_config.read(GpfTestCase.conf_dir_path / "test_authentifier.ini")

    def setUp(self) -> None:
        """fonction lancée avant chaque test de la classe"""
        # On détruit le singleton Authentifier
        Authentifier._instance = None

    @classmethod
    def tearDownClass(cls) -> None:
        """fonction lancée une fois après tous les tests de la classe"""
        super().tearDownClass()
        # On détruit le Singleton Config
        Config._instance = None

    def test_get_access_token_string_ok(self) -> None:
        """Vérifie le bon fonctionnement de get_access_token_string dans un cas normal."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Une authentification réussie
            o_mock.post(AuthentifierTestCase.url, json=AuthentifierTestCase.valid_token)
            # On tente de récupérer un token...
            s_token = Authentifier().get_access_token_string()
            # Il doit être ok
            self.assertEqual(s_token, "test_token")
            # On a dû faire une requête
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")
            # Vérifications sur l'historique (enfin ici y'a une requête...)
            o_history = o_mock.request_history
            # Requête 1 : vérification du type
            self.assertEqual(o_history[0].method.lower(), "post", "method == post")
            # Requête 1 : vérification du text
            s_text = "grant_type=password&username=TEST_LOGIN&password=TEST_PASSWORD&client_id=TEST_CLIENT_ID"
            self.assertEqual(o_history[0].text, s_text, "check text")

    def test_get_access_token_string_2_attempts(self) -> None:
        """Vérifie le bon fonctionnement de get_access_token_string si plusieurs tentatives."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Deux erreurs puis une authentification réussie
            o_mock.post(
                AuthentifierTestCase.url,
                [
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"json": AuthentifierTestCase.valid_token},
                ],
            )
            # On tente de récupérer un token...
            s_token = Authentifier().get_access_token_string()
            # Il doit être ok
            self.assertEqual(s_token, "test_token")
            # On a dû faire 3 requêtes
            self.assertEqual(o_mock.call_count, 3, "o_mock.call_count == 3")

    def test_get_access_token_string_too_much_attempts(self) -> None:
        """Vérifie le bon fonctionnement de get_access_token_string si trop de tentatives."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Trop d'erreurs
            o_mock.post(
                AuthentifierTestCase.url,
                [
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                ],
            )
            # On s'attend à une exception
            with self.assertRaises(AuthentificationError) as o_arc:
                # On tente de récupérer un token...
                Authentifier().get_access_token_string()
            # On doit avoir un message d'erreur
            self.assertEqual(o_arc.exception.message, "La récupération du jeton d'authentification a échoué après 3 tentatives")
            # On a dû faire 4 requêtes
            self.assertEqual(o_mock.call_count, 4, "o_mock.call_count == 4")

    def test_get_http_header(self) -> None:
        """Vérifie le bon fonctionnement de test_get_http_header."""
        # On mock get_access_token_string qui est déjà testée
        with patch.object(Authentifier, "get_access_token_string", return_value="test_token") as o_mock_method:
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

        # Vérifications o_mock_method
        # La fonction a été appelée
        self.assertTrue(o_mock_method.called)
        # Et ce 3 fois
        self.assertEqual(o_mock_method.call_count, 3)

    def test_revoke_token(self) -> None:
        """Vérifie le bon fonctionnement de revoke_token."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Une authentification réussie
            o_mock.post(AuthentifierTestCase.url, json=AuthentifierTestCase.valid_token)
            # On tente de récupérer un token...
            s_token = Authentifier().get_access_token_string()
            # Il doit être ok
            self.assertEqual(s_token, "test_token")
            # On a dû faire une requête
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")
            # On appel la fonction revoke_token à tester
            Authentifier().revoke_token()
            # On tente de re-récupérer un token...
            s_token = Authentifier().get_access_token_string()
            # Il doit être ok
            self.assertEqual(s_token, "test_token")
            # On a dû faire une seconde requête
            self.assertEqual(o_mock.call_count, 2, "o_mock.call_count == 2")
