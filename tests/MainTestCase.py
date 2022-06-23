from ignf_gpf_api.__main__ import parse_args
from tests.GpfTestCase import GpfTestCase


class MainTestCase(GpfTestCase):
    """Tests Main class.

    cmd : python3 -m unittest -b tests.MainTestCase
    """

    def test_parse_args(self) -> None:
        """Vérifie le bon fonctionnement de parse_args."""
        # Sans rien, ça quitte en erreur
        with self.assertRaises(SystemExit) as o_arc:
            parse_args([])
        self.assertEqual(o_arc.exception.code, 2)

        # Avec --help, ça quitte en succès
        with self.assertRaises(SystemExit) as o_arc:
            parse_args(["--help"])
        self.assertEqual(o_arc.exception.code, 0)

        # Avec --version, ça quitte en succès
        with self.assertRaises(SystemExit) as o_arc:
            parse_args(["--version"])
        self.assertEqual(o_arc.exception.code, 0)

    def test_parse_args_auth(self) -> None:
        """Vérifie le bon fonctionnement de parse_args."""
        # Avec tâche="auth" seul, c'est ok
        o_args = parse_args(["auth"])
        self.assertEqual(o_args.task, "auth")
        self.assertIsNone(o_args.show)

        # Avec tâche="auth" et show="token", c'est ok
        o_args = parse_args(["auth", "--show", "token"])
        self.assertEqual(o_args.task, "auth")
        self.assertEqual(o_args.show, "token")

        # Avec tâche "auth" et show="header", c'est ok
        o_args = parse_args(["auth", "--show", "header"])
        self.assertEqual(o_args.task, "auth")
        self.assertEqual(o_args.show, "header")

    def test_parse_args_config(self) -> None:
        """Vérifie le bon fonctionnement de parse_args."""
        # Avec tâche="config" seul, c'est ok
        o_args = parse_args(["config"])
        self.assertEqual(o_args.task, "config")
        self.assertIsNone(o_args.file)
        self.assertIsNone(o_args.section)
        self.assertIsNone(o_args.option)

        # Avec tâche="config" et file="toto.ini", c'est ok
        o_args = parse_args(["config", "--file", "toto.ini"])
        self.assertEqual(o_args.task, "config")
        self.assertEqual(o_args.file, "toto.ini")
        self.assertIsNone(o_args.section)
        self.assertIsNone(o_args.option)

        # Avec tâche "config", file="toto.ini" et section="store_authentification", c'est ok
        o_args = parse_args(["config", "--file", "toto.ini", "--section", "store_authentification"])
        self.assertEqual(o_args.task, "config")
        self.assertEqual(o_args.file, "toto.ini")
        self.assertEqual(o_args.section, "store_authentification")
        self.assertIsNone(o_args.option)

        # Avec tâche "config", section="store_authentification", c'est ok
        o_args = parse_args(["config", "--section", "store_authentification"])
        self.assertEqual(o_args.task, "config")
        self.assertIsNone(o_args.file)
        self.assertEqual(o_args.section, "store_authentification")
        self.assertIsNone(o_args.option)

        # Avec tâche "config", section="store_authentification" et option="password", c'est ok
        o_args = parse_args(["config", "--section", "store_authentification", "--option", "password"])
        self.assertEqual(o_args.task, "config")
        self.assertIsNone(o_args.file)
        self.assertEqual(o_args.section, "store_authentification")
        self.assertEqual(o_args.option, "password")
