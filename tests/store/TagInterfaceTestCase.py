import unittest

from ignf_gpf_api.store.TagInterface import TagInterface
from ignf_gpf_api.store.Errors import StoreEntityError


class TagInterfaceTestCase(unittest.TestCase):
    """Tests TagInterface class.

    cmd : python3 -m unittest -b tests.store.TagInterfaceTestCase
    """

    def test_init_getters(self) -> None:
        """Vérifie le bon fonctionnement du constructeur et des getters."""
        # Donnée renvoyée par l'API
        d_api_data = {
            "_id": "123456789",
            "name": "nom",
            "key": "value",
            "tags": {"tag_key": "tag_value"},
        }
        # Instanciation d'une Store entity
        o_tag_interface = TagInterface(d_api_data)

        # Vérifications
        # Le getter "get_tag" est ok
        self.assertEqual(o_tag_interface.get_tag("tag_key"), "tag_value")
        with self.assertRaises(StoreEntityError):
            o_tag_interface.get_tag("tag_not_existing")

    def test_api_add_tags(self) -> None:
        "Vérifie le bon fonctionnement de api_add_tags."

    def test_api_remove_tags(self) -> None:
        "Vérifie le bon fonctionnement de api_remove_tags."
