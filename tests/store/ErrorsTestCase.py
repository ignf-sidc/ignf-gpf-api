from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.store.Errors import StoreEntityError
from tests.GpfTestCase import GpfTestCase


class ErrorsTestCase(GpfTestCase):
    """Tests Errors classes.

    cmd : python3 -m unittest -b tests.store.ErrorsTestCase
    """

    @staticmethod
    def raise_store_entity_error() -> None:
        raise StoreEntityError("message")

    def test_store_entity_error(self) -> None:
        """Vérifie le bon fonctionnement de StoreEntityError."""
        # On lève l'exception
        with self.assertRaises(StoreEntityError) as o_arc:
            ErrorsTestCase.raise_store_entity_error()
        # Vérifications
        # Message renvoi message
        self.assertEqual(o_arc.exception.message, "message")
        # La forme str renvoi message
        self.assertEqual(str(o_arc.exception), "message")
        self.assertEqual(f"{o_arc.exception}", "message")
        # La représentation est le nom de classe + le message
        self.assertEqual(repr(o_arc.exception), "StoreEntityError(message)")
        # Enfant de GpfApiError
        self.assertIsInstance(o_arc.exception, GpfApiError)
