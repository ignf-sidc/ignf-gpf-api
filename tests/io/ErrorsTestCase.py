import unittest

from ignf_gpf_api.io.Errors import (
    ConfigReaderError,
    InternalServerError,
    NotAuthorizedError,
    NotFoundError,
    StatusCodeError,
    RouteNotFoundError,
)


class ErrorsTestCase(unittest.TestCase):
    """Tests Errors class : permet de vérifier que les erreurs peuvent bien s'instancier.

    cmd : python3 -m unittest -b tests.io.ErrorsTestCase
    """

    @staticmethod
    def raise_ConfigReaderError() -> None:
        raise ConfigReaderError("message")

    @staticmethod
    def raise_InternalServerError() -> None:
        raise InternalServerError("url", "method", {}, {})

    @staticmethod
    def raise_NotFoundError() -> None:
        raise NotFoundError("url", "method", {}, {})

    @staticmethod
    def raise_NotAuthorizedError() -> None:
        raise NotAuthorizedError("url", "method", {}, {}, "response")

    @staticmethod
    def raise_StatusCodeError() -> None:
        raise StatusCodeError("url", "method", {}, {}, 100, "response")

    @staticmethod
    def raise_RouteNotFoundError() -> None:
        raise RouteNotFoundError("route_name")

    def test_raise(self) -> None:
        """On vérifie que les erreurs fonctionnent bien."""
        self.assertRaises(ConfigReaderError, ErrorsTestCase.raise_ConfigReaderError)
        self.assertRaises(InternalServerError, ErrorsTestCase.raise_InternalServerError)
        self.assertRaises(NotFoundError, ErrorsTestCase.raise_NotFoundError)
        self.assertRaises(NotAuthorizedError, ErrorsTestCase.raise_NotAuthorizedError)
        self.assertRaises(StatusCodeError, ErrorsTestCase.raise_StatusCodeError)
        self.assertRaises(RouteNotFoundError, ErrorsTestCase.raise_RouteNotFoundError)
