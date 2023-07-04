from http import HTTPStatus
from io import BufferedReader
import json
from typing import Dict, Tuple
from unittest.mock import patch
import requests
import requests_mock

from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.auth.Authentifier import Authentifier
from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.io.Errors import RouteNotFoundError, ConflictError
from tests.GpfTestCase import GpfTestCase

# pylint:disable=protected-access


class ApiRequesterTestCase(GpfTestCase):
    """Tests ApiRequester class.

    cmd : python3 -m unittest -b tests.io.ApiRequesterTestCase
    """

    # On va mocker la classe d'authentification globalement
    o_mock_authentifier = patch.object(Authentifier, "get_access_token_string", return_value="test_token")

    # Paramètres de requêtes
    url = "https://api.test.io/"
    param = {
        "param_key_1": "value_1",
        "param_key_2": 2,
        "param_keys[]": ["pk1", "pk2", "pk3"],
    }
    encoded_param = "?param_key_1=value_1&param_key_2=2&param_keys%5B%5D=pk1&param_keys%5B%5D=pk2&param_keys%5B%5D=pk3"
    data = {
        "data_key_1": "value_1",
        "data_key_2": 2,
    }
    files: Dict[str, Tuple[str, BufferedReader]] = {}
    response = {"key": "value"}

    @classmethod
    def setUpClass(cls) -> None:
        """fonction lancée une fois avant tous les tests de la classe"""
        super().setUpClass()
        # On détruit le Singleton Config
        Config._instance = None
        # On charge une config spéciale pour les tests d'authentification
        o_config = Config()
        o_config.read(GpfTestCase.conf_dir_path / "test_requester.ini")
        # On mock la classe d'authentification
        cls.o_mock_authentifier.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """fonction lancée une fois après tous les tests de la classe"""
        super().tearDownClass()
        # On ne mock plus la classe d'authentification
        cls.o_mock_authentifier.stop()

    def test_route_request_ok(self) -> None:
        """Test de route_request quand la route existe."""
        # Instanciation d'une fausse réponse HTTP
        o_api_response = GpfTestCase.get_response()
        # On mock la fonction url_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester(), "url_request", return_value=o_api_response) as o_mock_request:
            # On effectue une requête
            o_fct_response = ApiRequester().route_request("test_create", {"id": 42}, ApiRequester.POST, params=self.param, data=self.data, files=self.files)
            # Vérification sur o_mock_request
            s_url = "https://api.test.io/api/v1/datastores/TEST_DATASTORE/create/42"
            o_mock_request.assert_called_once_with(s_url, ApiRequester.POST, self.param, self.data, self.files)
            # Vérification sur la réponse renvoyée par la fonction : ça doit être celle renvoyée par url_request
            self.assertEqual(o_fct_response, o_api_response)

    def test_route_request_ko(self) -> None:
        """Test de route_request quand la route n'existe pas."""
        # On veut vérifier que l'exception RouteNotFoundError est levée avec le bon nom de route non trouvée
        with self.assertRaises(RouteNotFoundError) as o_arc:
            # On effectue une requête
            ApiRequester().route_request("non_existing")
        # Vérifications
        self.assertEqual(o_arc.exception.route_name, "non_existing")

    def test_url_request_get(self) -> None:
        """Test de url_request dans le cadre d'une requête get."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Une requête réussie
            o_mock.get(self.url, json=self.response)
            # On effectue une requête
            o_response = ApiRequester().url_request(self.url, ApiRequester.GET, params=self.param, data=self.data)
            # Vérification sur la réponse
            self.assertDictEqual(o_response.json(), self.response)
            # On a dû faire une requête
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")
            # Vérifications sur l'historique (enfin ici y'a une requête...)
            o_history = o_mock.request_history
            # Requête 1 : vérification de l'url
            self.assertEqual(o_history[0].url, self.url + self.encoded_param, "check url")
            # Requête 1 : vérification du type
            self.assertEqual(o_history[0].method.lower(), "get", "method == get")
            # Requête 1 : vérification du corps de requête
            s_text = json.dumps(self.data)
            self.assertEqual(o_history[0].text, s_text, "check text")

    def test_url_request_post(self) -> None:
        """Test de url_request dans le cadre d'une requête post."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Une requête réussie
            o_mock.post(self.url, json=self.response)
            # On effectue une requête
            o_response = ApiRequester().url_request(self.url, ApiRequester.POST, params=self.param, data=self.data)
            # Vérification sur la réponse
            self.assertDictEqual(o_response.json(), self.response)
            # On a dû faire une requête
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")
            # Vérifications sur l'historique (enfin ici y'a une requête...)
            o_history = o_mock.request_history
            # Requête 1 : vérification de l'url
            self.assertEqual(o_history[0].url, self.url + self.encoded_param, "check url")
            # Requête 1 : vérification du type
            self.assertEqual(o_history[0].method.lower(), "post", "method == post")
            # Requête 1 : vérification du corps de requête
            s_text = json.dumps(self.data)
            self.assertEqual(o_history[0].text, s_text, "check text")

    def test_url_request_internal_server_error(self) -> None:
        """Test de url_request dans le cadre de 3 erreurs internes de suite."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Une requête non réussie
            o_mock.post(
                self.url,
                [
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                    {"status_code": HTTPStatus.INTERNAL_SERVER_ERROR},
                ],
            )
            # On s'attend à une exception
            with self.assertRaises(GpfApiError) as o_arc:
                # On effectue une requête
                ApiRequester().url_request(self.url, ApiRequester.POST, params=self.param, data=self.data)
            # On doit avoir un message d'erreur
            self.assertEqual(o_arc.exception.message, "L'exécution d'une requête a échoué après 3 tentatives")
            # On a dû faire 3 requêtes
            self.assertEqual(o_mock.call_count, 3, "o_mock.call_count == 3")

    def test_url_request_bad_request(self) -> None:
        """Test de url_request dans le cadre de 1 erreur bad request."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Une requête non réussie
            o_mock.post(self.url, status_code=HTTPStatus.BAD_REQUEST)
            # On s'attend à une exception
            with self.assertRaises(GpfApiError) as o_arc:
                # On effectue une requête
                ApiRequester().url_request(self.url, ApiRequester.POST, params=self.param, data=self.data)
            # On doit avoir un message d'erreur
            self.assertEqual(o_arc.exception.message, "La requête formulée par le programme est incorrecte. Contactez le support.")
            # On a dû faire 1 seule requête
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")

    def test_url_request_conflict(self) -> None:
        """Test de url_request dans le cadre de 1 erreur conflict."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Une requête non réussie
            o_mock.post(self.url, status_code=HTTPStatus.CONFLICT)
            # On s'attend à une exception
            with self.assertRaises(ConflictError):
                # On effectue une requête
                ApiRequester().url_request(self.url, ApiRequester.POST, params=self.param, data=self.data)
            # On doit avoir un message d'erreur
            # self.assertEqual(o_arc.exception.message, "La requête envoyée à l'Entrepôt génère un conflit. N'avez-vous pas déjà effectué l'action que vous essayez de faire ?")
            # Au contraire de GpfApiError, ConflictError ne comporte pas de membre message...
            # On a dû faire 1 seule requête
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")

    def test_url_request_not_found(self) -> None:
        """Test de url_request dans le cadre d'une erreur 404 (not found)."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            # Une requête non réussie
            o_mock.post(
                self.url,
                [
                    {"status_code": HTTPStatus.NOT_FOUND},
                    {"status_code": HTTPStatus.NOT_FOUND},
                    {"status_code": HTTPStatus.NOT_FOUND},
                ],
            )
            # On s'attend à une exception
            with self.assertRaises(GpfApiError) as o_arc:
                # On effectue une requête
                ApiRequester().url_request(self.url, ApiRequester.POST, params=self.param, data=self.data)
            # On doit avoir un message d'erreur explicite
            s_message = f"L'élément demandé n'existe pas. Contactez le support si vous n'êtes pas à l'origine de la demande. URL : {self.url}."
            self.assertEqual(o_arc.exception.message, s_message)
            # On a dû faire 1 seule requête (sortie immédiate dans ce cas)
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")

    def test_url_request_not_authorized(self) -> None:
        """Test de url_request dans le cadre d'une erreur 403 ou 401 (not authorized)."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            with patch.object(Authentifier(), "revoke_token", return_value=None) as o_mock_revoke_token:
                # Une requête avec comme codes retour 104, 403 puis 200
                o_mock.post(
                    self.url,
                    [
                        {"status_code": HTTPStatus.UNAUTHORIZED},
                        {"status_code": HTTPStatus.FORBIDDEN},
                        {"status_code": HTTPStatus.OK},
                    ],
                )
                # Lancement de la requête
                ApiRequester().url_request(self.url, ApiRequester.POST, params=self.param, data=self.data)
                # On a dû faire 3 requêtes
                self.assertEqual(o_mock.call_count, 3, "o_mock.call_count == 3")
                # On a dû faire 2 appels à revoke_token
                self.assertEqual(o_mock_revoke_token.call_count, 2, "o_mock_revoke_token.call_count == 2")

    def test_url_request_http_error(self) -> None:
        """Test de url_request dans le cadre où on a une HTTPError."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            o_mock.get(self.url, exc=requests.HTTPError)
            # On s'attend à une exception
            with self.assertRaises(GpfApiError) as o_arc:
                # Lancement de la requête
                ApiRequester().url_request(self.url, ApiRequester.GET, params=self.param, data=self.data)
            # On doit avoir un message d'erreur
            self.assertEqual(o_arc.exception.message, "L'url indiquée en configuration est invalide ou inexistante. Contactez le support.")
            # On a dû faire 1 seule requête
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")

    def test_url_request_url_required(self) -> None:
        """Test de url_request dans le cadre où on a une URLRequired."""
        # On mock...
        with requests_mock.Mocker() as o_mock:
            o_mock.get(self.url, exc=requests.URLRequired)
            # On s'attend à une exception
            with self.assertRaises(GpfApiError) as o_arc:
                # Lancement de la requête
                ApiRequester().url_request(self.url, ApiRequester.GET, params=self.param, data=self.data)
            # On doit avoir un message d'erreur
            self.assertEqual(o_arc.exception.message, "L'url indiquée en configuration est invalide ou inexistante. Contactez le support.")
            # On a dû faire 1 seule requête
            self.assertEqual(o_mock.call_count, 1, "o_mock.call_count == 1")

    def test_range_next_page(self) -> None:
        """Test de range_next_page."""
        # On a 10 entités à récupérer et on en a récupéré 10 : on ne doit pas continuer
        self.assertFalse(ApiRequester.range_next_page("1-10/10", 10))
        # On a 10 entités à récupérer et on en a récupéré 5 : on doit continuer
        self.assertTrue(ApiRequester.range_next_page("1-5/10", 5))
        # Content-Range nul : on doit s'arrêter
        self.assertFalse(ApiRequester.range_next_page(None, 5))
        # Content-Range non parsable : on doit s'arrêter
        self.assertFalse(ApiRequester.range_next_page("non_parsable", 0))
