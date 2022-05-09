import json
import unittest

from ignf_gpf_api.store.StoreEntity import StoreEntity


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

    def test_api_create(self) -> None:
        "Vérifie le bon fonctionnement de api_create."

    def test_api_list(self) -> None:
        "Vérifie le bon fonctionnement de api_list."

    def test_api_delete(self) -> None:
        "Vérifie le bon fonctionnement de api_delete."
