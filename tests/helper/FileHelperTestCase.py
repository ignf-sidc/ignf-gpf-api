from ignf_gpf_api.helper.FileHelper import FileHelper
from tests.GpfTestCase import GpfTestCase


class FileHelperTestCase(GpfTestCase):
    """Test de la classe FileHelper.

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

    def test_md5_hash(self) -> None:
        """Vérification du bon fonctionnement de la fonction md5_hash."""
        self.assertEqual("54b63bf2c922188c1f19abe97e865005", FileHelper.md5_hash(GpfTestCase.test_dir_path / "helper" / "FileHelper" / "md5.txt"))
