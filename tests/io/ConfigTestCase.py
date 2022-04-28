#! /usr/bin/env python3

# cSpell:ignore BDTOPO

import configparser
from pathlib import Path
import unittest

from ignf_gpf_api.io.Config import Config


class ConfigTestCase(unittest.TestCase):
    """Tests ConfigTestCase class.

    cmd : python3 -m unittest -b ignf_gpf_api.tests.io.ConfigTestCase
    """

    config_path = Path(__file__).parent.parent / "_config"

    def test_get_parser(self) -> None:
        """Vérifie le bon fonctionnement de get_parser."""
        # On vérifie le type de get_parser
        self.assertIsInstance(Config().get_parser(), configparser.ConfigParser)

    def test_read(self) -> None:
        """Vérifie le bon fonctionnement de read."""
        cParser = Config().get_parser()
        # On vérifie que l'on a les valeurs par défaut
        self.assertEqual(cParser.get("store_authentification", "login"), "LOGIN_TO_MODIFY")
        self.assertEqual(cParser.get("store_authentification", "password"), "PASSWORD_TO_MODIFY")
        self.assertEqual(cParser.get("store_api", "datastore"), "DATASTORE_ID_TO_MODIFY")
        # On ouvre le nouveau fichier
        Config().read(ConfigTestCase.config_path / "test_overload.ini")
        # On vérifie que l'on a les nouvelles valeurs
        self.assertEqual(cParser.get("store_authentification", "login"), "TEST_LOGIN")
        self.assertEqual(cParser.get("store_authentification", "password"), "TEST_PASSWORD")
        self.assertEqual(cParser.get("store_api", "datastore"), "TEST_DATASTORE")

    def test_get(self) -> None:
        """Vérifie le bon fonctionnement de get, get_int, get_float et get_bool."""
        Config().read(ConfigTestCase.config_path / "test_value_type.ini")
        # On peut récupérer des strings
        self.assertEqual(Config().get("test_value_type", "my_string"), "titi")
        self.assertEqual(Config().get("test_value_type", "my_int"), "42")
        self.assertEqual(Config().get("test_value_type", "my_float"), "4.2")
        self.assertEqual(Config().get("test_value_type", "my_bool"), "true")
        # Ou le type adapté
        self.assertEqual(Config().get_int("test_value_type", "my_int"), 42)
        self.assertEqual(Config().get_float("test_value_type", "my_float"), 4.2)
        self.assertEqual(Config().get_bool("test_value_type", "my_bool"), True)
        # On a la valeur par défaut si non existant
        self.assertIsNone(Config().get("test_value_type", "not_existing", fallback=None))
        self.assertIsNone(Config().get_int("test_value_type", "not_existing", fallback=None))
        self.assertIsNone(Config().get_float("test_value_type", "not_existing", fallback=None))
        self.assertIsNone(Config().get_bool("test_value_type", "not_existing", fallback=None))
        self.assertEqual(Config().get("test_value_type", "not_existing", fallback="fallback"), "fallback")
        self.assertEqual(Config().get_int("test_value_type", "not_existing", fallback=42), 42)
        self.assertEqual(Config().get_float("test_value_type", "not_existing", fallback=4.2), 4.2)
        self.assertEqual(Config().get_bool("test_value_type", "not_existing", fallback=True), True)

    def test_same_instance(self) -> None:
        """Même instance."""
        # Première instance
        cConfig_1 = Config()
        # Deuxième instance
        cConfig_2 = Config()
        # Ca doit être les mêmes
        self.assertEqual(cConfig_1, cConfig_2)
