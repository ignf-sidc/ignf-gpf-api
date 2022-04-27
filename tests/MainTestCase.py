import unittest

from ignf_gpf_api.__main__ import parse_args


class MainTestCase(unittest.TestCase):
    """Tests ConfigTestCase class.

    cmd : python3 -m unittest -b tests.MainTestCase
    """

    def test_parse_args(self) -> None:
        """Vérifie le bon fonctionnement de parse_args."""
        # Sans rien, ça quitte en erreur
        with self.assertRaises(SystemExit) as cArc:
            parse_args([])
        self.assertEqual(cArc.exception.code, 2)

        # Avec --help, ça quitte en succès
        with self.assertRaises(SystemExit) as cArc:
            parse_args(["--help"])
        self.assertEqual(cArc.exception.code, 0)

        # Avec --version, ça quitte en succès
        with self.assertRaises(SystemExit) as cArc:
            parse_args(["--version"])
        self.assertEqual(cArc.exception.code, 0)

    def test_parse_args_auth(self) -> None:
        """Vérifie le bon fonctionnement de parse_args."""
        # Avec tâche="auth" seul, c'est ok
        cArgs = parse_args(["auth"])
        self.assertEqual(cArgs.task, "auth")
        self.assertIsNone(cArgs.show)

        # Avec tâche="auth" et show="token", c'est ok
        cArgs = parse_args(["auth", "--show", "token"])
        self.assertEqual(cArgs.task, "auth")
        self.assertEqual(cArgs.show, "token")

        # Avec tâche "auth" et show="header", c'est ok
        cArgs = parse_args(["auth", "--show", "header"])
        self.assertEqual(cArgs.task, "auth")
        self.assertEqual(cArgs.show, "header")

    def test_parse_args_config(self) -> None:
        """Vérifie le bon fonctionnement de parse_args."""
        # Avec tâche="config" seul, c'est ok
        cArgs = parse_args(["config"])
        self.assertEqual(cArgs.task, "config")
        self.assertIsNone(cArgs.file)
        self.assertIsNone(cArgs.section)
        self.assertIsNone(cArgs.option)

        # Avec tâche="config" et file="toto.ini", c'est ok
        cArgs = parse_args(["config", "--file", "toto.ini"])
        self.assertEqual(cArgs.task, "config")
        self.assertEqual(cArgs.file, "toto.ini")
        self.assertIsNone(cArgs.section)
        self.assertIsNone(cArgs.option)

        # Avec tâche "config", file="toto.ini" et section="store_authentification", c'est ok
        cArgs = parse_args(["config", "--file", "toto.ini", "--section", "store_authentification"])
        self.assertEqual(cArgs.task, "config")
        self.assertEqual(cArgs.file, "toto.ini")
        self.assertEqual(cArgs.section, "store_authentification")
        self.assertIsNone(cArgs.option)

        # Avec tâche "config", section="store_authentification", c'est ok
        cArgs = parse_args(["config", "--section", "store_authentification"])
        self.assertEqual(cArgs.task, "config")
        self.assertIsNone(cArgs.file)
        self.assertEqual(cArgs.section, "store_authentification")
        self.assertIsNone(cArgs.option)

        # Avec tâche "config", section="store_authentification" et option="password", c'est ok
        cArgs = parse_args(["config", "--section", "store_authentification", "--option", "password"])
        self.assertEqual(cArgs.task, "config")
        self.assertIsNone(cArgs.file)
        self.assertEqual(cArgs.section, "store_authentification")
        self.assertEqual(cArgs.option, "password")
