import configparser
from pathlib import Path

from ignf_gpf_api.io.Config import Config
from tests.GpfTestCase import GpfTestCase

# pylint:disable=protected-access


class ConfigTestCase(GpfTestCase):
    """Tests ConfigTestCase class.

    cmd : python3 -m unittest -b tests.io.ConfigTestCase
    """

    def setUp(self) -> None:
        # On détruit le singleton Config
        Config._instance = None

    def test_get_parser(self) -> None:
        """Vérifie le bon fonctionnement de get_parser."""
        # On vérifie le type de get_parser
        self.assertIsInstance(Config().get_parser(), configparser.ConfigParser)

    def test_read(self) -> None:
        """Vérifie le bon fonctionnement de read."""
        o_parser = Config().get_parser()
        # On vérifie que l'on a les valeurs par défaut
        self.assertEqual(o_parser.get("store_authentification", "login"), "LOGIN_TO_MODIFY")
        self.assertEqual(o_parser.get("store_authentification", "password"), "PASSWORD_TO_MODIFY")
        self.assertEqual(o_parser.get("store_api", "datastore"), "DATASTORE_ID_TO_MODIFY")
        # On ouvre le nouveau fichier
        Config().read(GpfTestCase.conf_dir_path / "test_overload.ini")
        # On vérifie que l'on a les nouvelles valeurs
        self.assertEqual(o_parser.get("store_authentification", "login"), "TEST_LOGIN")
        self.assertEqual(o_parser.get("store_authentification", "password"), "TEST_PASSWORD")
        self.assertEqual(o_parser.get("store_api", "datastore"), "TEST_DATASTORE")

    def test_get(self) -> None:
        """Vérifie le bon fonctionnement de get, get_int, get_float et get_bool."""
        Config().read(GpfTestCase.conf_dir_path / "test_value_type.ini")
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

    def test_get_temp(self) -> None:
        """Vérifie le bon fonctionnement de get_temp."""
        self.assertEqual(Config().get_temp(), Path("/tmp"))

    def test_same_instance(self) -> None:
        """Même instance."""
        # Première instance
        o_config_1 = Config()
        # Deuxième instance
        o_config_2 = Config()
        # Ca doit être les mêmes
        self.assertEqual(o_config_1, o_config_2)
