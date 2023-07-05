from unittest.mock import patch

from ignf_gpf_api.store.Datastore import Datastore
from ignf_gpf_api.io.ApiRequester import ApiRequester
from tests.GpfTestCase import GpfTestCase


class DatastoreTestCase(GpfTestCase):
    """Tests Upload class.

    cmd : python3 -m unittest -b tests.store.DataDatastoreTestCase
    """

    json_request = {
        "communities_member": [
            {"community": {"datastore": "1", "name": "Datastore 1", "technical_name": "ds1"}},
            {"community": {"datastore": "2", "name": "Datastore 2", "technical_name": "ds2"}},
        ]
    }

    def test_api_list_all(self) -> None:
        """Vérifie le bon fonctionnement de api_list."""
        # On a une réponse renvoyant 2 entités
        o_response = GpfTestCase.get_response(json=DatastoreTestCase.json_request)
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester(), "route_request", return_value=o_response) as o_mock_request:
            # On effectue le listing d'une entité
            l_entities = Datastore.api_list()
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("user_get")
            # Vérifications sur l_entities
            self.assertIsInstance(l_entities, list)
            self.assertEqual(len(l_entities), 2)
            for i, o_entity in enumerate(l_entities, start=1):
                self.assertIsInstance(o_entity, Datastore)
                self.assertEqual(o_entity.id, str(i))
                self.assertEqual(o_entity["name"], DatastoreTestCase.json_request["communities_member"][i - 1]["community"]["name"])
                self.assertEqual(o_entity["technical_name"], DatastoreTestCase.json_request["communities_member"][i - 1]["community"]["technical_name"])

    def test_api_list_filer_name(self) -> None:
        """Vérifie le bon fonctionnement de api_list quand on fait un filtre sur le nom."""
        # On a une réponse renvoyant 2 entités et on ne doit en conserver qu'une
        o_response = GpfTestCase.get_response(json=DatastoreTestCase.json_request)
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester(), "route_request", return_value=o_response) as o_mock_request:
            # On effectue le listing d'une entité
            l_entities = Datastore.api_list({"name": "Datastore 2"})
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("user_get")
            # Vérifications sur l_entities
            self.assertIsInstance(l_entities, list)
            self.assertEqual(len(l_entities), 1)
            self.assertIsInstance(l_entities[0], Datastore)
            self.assertEqual(l_entities[0].id, "2")
            self.assertEqual(l_entities[0]["name"], "Datastore 2")
            self.assertEqual(l_entities[0]["technical_name"], "ds2")

    def test_api_list_filer_technical_name(self) -> None:
        """Vérifie le bon fonctionnement de api_list quand on fait un filtre sur le nom technique."""
        # On a une réponse renvoyant 2 entités et on ne doit en conserver qu'une
        o_response = GpfTestCase.get_response(json=DatastoreTestCase.json_request)
        # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(ApiRequester(), "route_request", return_value=o_response) as o_mock_request:
            # On effectue le listing d'une entité
            l_entities = Datastore.api_list({"name": "ds1"})
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("user_get")
            # Vérifications sur l_entities
            self.assertIsInstance(l_entities, list)
            self.assertEqual(len(l_entities), 1)
            self.assertIsInstance(l_entities[0], Datastore)
            self.assertEqual(l_entities[0].id, "1")
            self.assertEqual(l_entities[0]["name"], "Datastore 1")
            self.assertEqual(l_entities[0]["technical_name"], "ds1")
