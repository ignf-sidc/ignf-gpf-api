from ignf_gpf_api.Errors import GpfApiError
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.io.Dataset import Dataset
from ignf_gpf_api.io.DescriptorFileReader import DescriptorFileReader

from tests.GpfTestCase import GpfTestCase


class DescriptorFileReaderTestCase(GpfTestCase):
    """Test de la classe DescriptorFileReader.

    cmd : python3 -m unittest -b tests.io.DescriptorFileReaderTestCase
    """

    def test_init_ok_1(self) -> None:
        """Test du constructeur quand tout va bien n°1."""
        # Ouverture
        o_dsr = DescriptorFileReader(Config.data_dir_path / "datasets" / "1_dataset_vector" / "upload_descriptor.json")
        # Vérifications
        self.assertEqual(len(o_dsr.datasets), 1)
        self.assertIsInstance(o_dsr.datasets[0], Dataset)

    def test_init_ok_2(self) -> None:
        """Test du constructeur quand tout va bien n°2."""
        # Ouverture
        o_dsr = DescriptorFileReader(Config.data_dir_path / "datasets" / "2_dataset_archive" / "upload_descriptor.json")
        # Vérifications
        self.assertEqual(len(o_dsr.datasets), 1)
        self.assertEqual(o_dsr.datasets[0].upload_infos["name"], "EXAMPLE_DATASET_ARCHIVE")

    def test_init_ko_dir_not_found(self) -> None:
        """Test du constructeur quand au moins un dossier indiqué n'est pas trouvé."""
        with self.assertRaises(GpfApiError) as o_arc:
            # Ouverture
            DescriptorFileReader(GpfTestCase.data_dir_path / "datasets" / "1_test_dataset_bad_pathes" / "upload_descriptor.json")
        # Vérifications
        self.assertEqual(o_arc.exception.message, "Au moins un des répertoires listés dans le fichier descripteur de livraison n'existe pas.")
