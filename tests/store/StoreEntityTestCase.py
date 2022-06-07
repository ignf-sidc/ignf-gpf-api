import json
import unittest
from unittest.mock import patch
import requests
import requests_mock

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.io.ApiRequester import ApiRequester


class StoreEntityTestCase(unittest.TestCase):
    """Tests StoreEntity class.

    cmd : python3 -m unittest -b tests.store.StoreEntityTestCase
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
        o_store_entity = StoreEntity(d_api_data)

        # Vérifications
        # On a bien un comportement de dictionnaire
        self.assertEqual(o_store_entity["key"], "value")
        # Le getter "id" est ok
        self.assertEqual(o_store_entity.id, "123456789")
        # Le getter "get_store_properties" est ok
        self.assertDictEqual(o_store_entity.get_store_properties(), d_api_data)
        # Le getter "to_json" est ok
        s_json = o_store_entity.to_json()
        self.assertIsInstance(s_json, str)
        self.assertEqual(s_json, json.dumps(d_api_data))
        s_json = o_store_entity.to_json(indent=4)
        self.assertIsInstance(s_json, str)
        self.assertEqual(s_json, json.dumps(d_api_data, indent=4))
        # La représentation est ok
        self.assertEqual(str(o_store_entity), "StoreEntity(id=123456789, name=nom)")
        self.assertEqual(str(StoreEntity({"_id": "123456789"})), "StoreEntity(id=123456789)")

    def test_filter_dict_from_str(self) -> None:
        """Vérifie le bon fonctionnement de filter_dict_from_str."""
        # On teste avec ou sans espace
        d_tests = {
            "cle1=valeur1, cle2=valeur2, cle3=valeur3": {"cle1": "valeur1", "cle2": "valeur2", "cle3": "valeur3"},
            "cle1=valeur1, cle2 = valeur2, cle3=valeur3": {"cle1": "valeur1", "cle2": "valeur2", "cle3": "valeur3"},
            " cle1=valeur1,cle2=valeur2,cle3=valeur3 ": {"cle1": "valeur1", "cle2": "valeur2", "cle3": "valeur3"},
        }
        # On itère sur la liste de tests
        for s_key, d_value in d_tests.items():
            d_parsed = StoreEntity.filter_dict_from_str(s_key)
            self.assertIsInstance(d_parsed, dict)
            self.assertDictEqual(d_value, d_parsed, s_key)

    def test_api_get_ok(self) -> None:
        "Vérifie le bon fonctionnement de api_get si tout va bien."

    def test_api_get_not_found(self) -> None:
        "Vérifie le bon fonctionnement de api_get si entité non trouvé."

    def test_api_create_1(self) -> None:
        "Vérifie le bon fonctionnement de api_create sans route_params."
        # on créé un store entity dans l'api (avec un dictionnaire)
        # on vérifie que la fct de creation a bien instancié le store entity avec le dictionnaire envoyé
        # 1/ on vérifie l'appel ApiRequester.route_request
        # 2/ on vérifie l'objet instancié

        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker() as o_mock:
            o_mock.post("http://test.com/", json={"_id": "123456789"})
            o_response = requests.request("POST", "http://test.com/")
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            # On effectue la création d'un objet
            o_store_entity = StoreEntity.api_create({"key_1": "value_1"})
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_create",
                route_params=None,
                method=ApiRequester.POST,
                data={"key_1": "value_1"},
            )
            # Vérifications sur o_store_entity
            self.assertIsInstance(o_store_entity, StoreEntity)
            self.assertEqual(o_store_entity.id, "123456789")

    def test_api_create_2(self) -> None:
        "Vérifie le bon fonctionnement de api_create avec route_params."
        # on créé un store entity dans l'api (avec un dictionnaire)
        # on vérifie que la fct de creation a bien instancié le store entity avec le dictionnaire envoyé
        # 1/ on vérifie l'appel ApiRequester.route_request
        # 2/ on vérifie l'objet instancié

        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker() as o_mock:
            o_mock.post("http://test.com/", json={"_id": "123456789"})
            o_response = requests.request("POST", "http://test.com/")
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            # On effectue la création d'un objet
            o_store_entity = StoreEntity.api_create({"key_1": "value_1"}, route_params={"toto": "titi"})
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with(
                "store_entity_create",
                route_params={"toto": "titi"},
                method=ApiRequester.POST,
                data={"key_1": "value_1"},
            )
            # Vérifications sur o_store_entity
            self.assertIsInstance(o_store_entity, StoreEntity)
            self.assertEqual(o_store_entity.id, "123456789")

    def test_api_list(self) -> None:
        "Vérifie le bon fonctionnement de api_list."

    def test_api_delete(self) -> None:
        "Vérifie le bon fonctionnement de api_delete."
        # on créé une instance puis on la supprime
        # 1/ on vérifie l'appel ApiRequester.route_request
        # 2/ avec le mock, pas besoin de vérifier que l'instance (SUR l'api) n'existe plus

        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=None) as o_mock_request:
            # On effectue la suppression d'une entité
            # On instancie une entité à supprimer
            o_store_entity = StoreEntity({"_id": "id_à_supprimer"})
            # On appelle la fonction api_delete
            o_store_entity.api_delete()
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("store_entity_delete", route_params={"store_entity": "id_à_supprimer"}, method=ApiRequester.DELETE)

    def test_api_update(self) -> None:
        "Vérifie le bon fonctionnement de api_update."
        # Infos de l'entité avant la maj et après
        d_old_data = {"_id": "id_à_maj", "name": "ancien nom"}
        d_new_data = {"_id": "id_à_maj", "name": "nouveau nom"}
        # Instanciation d'une fausse réponse HTTP
        with requests_mock.Mocker() as o_mock:
            o_mock.post("http://test.com/", json=d_new_data)
            o_response = requests.request("POST", "http://test.com/")
        # Instanciation du ApiRequester
        o_api_requester = ApiRequester()
        # On mock la fonction request, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(o_api_requester, "route_request", return_value=o_response) as o_mock_request:
            # On effectue la suppression d'une entité
            # On instancie une entité à mettre à jour
            o_store_entity = StoreEntity(d_old_data)
            # Les info de l'entité sont celles à mettre à jour
            self.assertDictEqual(o_store_entity.get_store_properties(), d_old_data)
            # On appelle la fonction api_update
            o_store_entity.api_update()
            # Vérification sur o_mock_request
            o_mock_request.assert_called_once_with("store_entity_get", route_params={"store_entity": "id_à_maj"})
            # Vérification que les infos de l'entité sont maj
            self.assertDictEqual(o_store_entity.get_store_properties(), d_new_data)
