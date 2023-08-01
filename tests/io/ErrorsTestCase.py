from ignf_gpf_api.io.Errors import (
    _WithResponseError,
    ConfigReaderError,
    ConflictError,
    InternalServerError,
    NotAuthorizedError,
    NotFoundError,
    StatusCodeError,
    RouteNotFoundError,
)
from tests.GpfTestCase import GpfTestCase


class ErrorsTestCase(GpfTestCase):
    """Tests Errors class : permet de vérifier que les erreurs peuvent bien s'instancier.

    cmd : python3 -m unittest -b tests.io.ErrorsTestCase
    """

    @staticmethod
    def raise_config_reader_error() -> None:
        raise ConfigReaderError("message")

    @staticmethod
    def raise_internal_server_error() -> None:
        raise InternalServerError("url", "method", {}, {})

    @staticmethod
    def raise_not_found_error() -> None:
        raise NotFoundError("url", "method", {}, {}, "response")

    @staticmethod
    def raise_not_authorized_error() -> None:
        raise NotAuthorizedError("url", "method", {}, {}, "response")

    @staticmethod
    def raise_conflict_error() -> None:
        raise ConflictError("url", "method", {}, {}, "response")

    @staticmethod
    def raise_status_code_error() -> None:
        raise StatusCodeError("url", "method", {}, {}, 100, "response")

    @staticmethod
    def raise_route_not_found_error() -> None:
        raise RouteNotFoundError("route_name")

    def test_raise(self) -> None:
        """On vérifie que les erreurs fonctionnent bien."""
        self.assertRaises(ConfigReaderError, ErrorsTestCase.raise_config_reader_error)
        self.assertRaises(InternalServerError, ErrorsTestCase.raise_internal_server_error)
        self.assertRaises(NotFoundError, ErrorsTestCase.raise_not_found_error)
        self.assertRaises(NotAuthorizedError, ErrorsTestCase.raise_not_authorized_error)
        self.assertRaises(ConflictError, ErrorsTestCase.raise_conflict_error)
        self.assertRaises(StatusCodeError, ErrorsTestCase.raise_status_code_error)
        self.assertRaises(RouteNotFoundError, ErrorsTestCase.raise_route_not_found_error)

    def test_message(self) -> None:
        """On vérifie que le message est bien récupéré quand c'est possible ou
        que le message par défaut est bien indiqué sinon.
        """
        # Text non parsable -> message par défaut
        e_error = _WithResponseError("url", "method", {}, {}, "response")
        self.assertEqual(e_error.message, "Pas d'indication spécifique indiquée par l'API.")
        # Pas de clé 'error_description' -> message par défaut
        e_error = _WithResponseError("url", "method", {}, {}, '{"error_description_?_et_non_ce_n_est_pas_la_bonne_clef":false}')
        self.assertEqual(e_error.message, "Pas d'indication spécifique indiquée par l'API.")
        # Clé 'error_description' -> message récupéré
        e_error = _WithResponseError("url", "method", {}, {}, '{"error_description": ["un beau message"]}')
        self.assertEqual(e_error.message, "un beau message")
        # Clé 'error_description' -> messages récupérés
        e_error = _WithResponseError("url", "method", {}, {}, '{"error_description": ["un beau message", "et de deux"]}')
        self.assertEqual(e_error.message, "un beau message\net de deux")
