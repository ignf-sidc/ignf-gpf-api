from unittest.mock import patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.interface.TagInterface import TagInterface
from ignf_gpf_api.store.Errors import StoreEntityError
from tests.GpfTestCase import GpfTestCase


class TagInterfaceTestCase(GpfTestCase):
    """Tests TagInterface class.

    cmd : python3 -m unittest -b tests.store.interface.TagInterfaceTestCase
    """

    def test_init_getters(self) -> None:
        """Vérifie le bon fonctionnement du constructeur et des getters."""
        # Donnée renvoyée par l'API
        d_api_data = {
            "_id": "123456789",
            "tags": {"tag_key": "tag_value"},
        }
        # Instanciation d'une Store entity
        o_tag_interface = TagInterface(d_api_data)

        # Vérifications
        # Le getter sur "tag_key" est ok
        self.assertEqual(o_tag_interface.get_tag("tag_key"), "tag_value")
        # Le getter sur "tag_not_existing" est nok
        with self.assertRaises(StoreEntityError):
            o_tag_interface.get_tag("tag_not_existing")

    def test_api_add_tags(self) -> None:
        "Vérifie le bon fonctionnement de api_add_tags."
        # créer une instance TagInterface
        # 1/ on vérifie l'appel ApiRequester.route_request
        # 2/ on ne peut pas vérifier l'objet instancié

        # Donnée renvoyée par l'API
        d_api_data = {
            "_id": "123456789",
            "tags": {"tag_key": "tag_value"},
        }
        # dictionnaire de tag à ajouter
        d_more_tag_data = {"tag_key2": "tag_value2"}

        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On instancie un TagInterface
            o_tag_interface = TagInterface(d_api_data)
            # On appelle la fonction api_add_tags
            o_tag_interface.api_add_tags(d_more_tag_data)
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_add_tags",
                route_params={"store_entity": "123456789"},
                method=ApiRequester.POST,
                data=d_more_tag_data,
            )

    def test_api_remove_tags(self) -> None:
        "Vérifie le bon fonctionnement de api_remove_tags."
        # on créé une instance TagInterface puis on appelle la fct api_remove_tag
        # 1/ on vérifie l'appel ApiRequester.route_request
        # 2/ avec le mock, pas besoin de verifier que l'instance (SUR l'api) n'existe plus

        # Donnée renvoyée par l'API
        d_api_data = {
            "_id": "123456789",
            "tags": {"tag_key": "tag_value", "tag_key2": "tag_value2"},
        }
        # dictionnaire de tag à supprimer
        l_less_tag_data = ["tag_key2"]

        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester, "route_request", return_value=None) as o_mock_request:
            # On instancie un TagInterface
            o_tag_interface = TagInterface(d_api_data)
            # On appelle la fonction api_remove_tags
            o_tag_interface.api_remove_tags(l_less_tag_data)
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_delete_tags",
                route_params={"store_entity": "123456789"},
                method=ApiRequester.DELETE,
                params={"tags[]": l_less_tag_data},
            )
