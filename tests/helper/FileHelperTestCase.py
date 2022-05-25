import unittest

from ignf_gpf_api.helper.FileHelper import FileHelper


class FileHelperTestCase(unittest.TestCase):
    """Test de la classe JsonHelper : on doit pouvoir ouvrir des JSON avec des commentaires !
    Et on doit pouvoir valider des schéma JSON avec des messages précis selon l'erreur.

    cmd : python3 -m unittest -b tests.helper.FileHelperTestCase
    """

    def test_format_size(self) -> None:
        """Vérification du bon fonctionnement de la fonction format_size."""
        self.assertEqual("1 octet", FileHelper.format_size(1))
        self.assertEqual("500 octets", FileHelper.format_size(500))
        self.assertEqual("488.28 KO", FileHelper.format_size(500000))
        self.assertEqual("476.84 MO", FileHelper.format_size(500000000))
        self.assertEqual("465.66 GO", FileHelper.format_size(500000000000))
        self.assertEqual("454.75 TO", FileHelper.format_size(500000000000000))
