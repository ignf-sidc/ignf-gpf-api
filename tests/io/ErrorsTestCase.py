from ignf_gpf_api.io.Errors import (
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
        raise NotFoundError("url", "method", {}, {})

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
