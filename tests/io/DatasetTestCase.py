from pathlib import Path

from ignf_gpf_api.helper.FileHelper import FileHelper
from ignf_gpf_api.helper.JsonHelper import JsonHelper
from ignf_gpf_api.io.Dataset import Dataset

from tests.GpfTestCase import GpfTestCase


class DatasetTestCase(GpfTestCase):
    """Test de la classe Dataset.

    cmd : python3 -m unittest -b tests.io.DatasetTestCase
    """

    def test_init(self) -> None:
        """Test du constructeur."""
        self.maxDiff = None
        # Ouverture et chemins
        p_descriptor = GpfTestCase.data_dir_path / "datasets" / "3_test_dataset_sub_dir" / "upload_descriptor.json"
        p_root = p_descriptor.parent
        d_descriptor = JsonHelper.load(p_descriptor)
        d_dataset = d_descriptor["datasets"][0]
        p_md5 = p_root / "CANTON.md5"
        # Suppression du fichier md5 (les tests doivent le régénérer)
        p_md5.unlink(missing_ok=True)
        self.assertFalse(p_md5.exists(), "CANTON.md5 existe")
        # Instanciation
        o_dataset = Dataset(d_dataset, p_root)
        # Vérifications
        self.assertEqual(o_dataset.data_dirs, [Path(i) for i in d_dataset["data_dirs"]])
        self.assertDictEqual(o_dataset.upload_infos, d_dataset["upload_infos"])
        self.assertListEqual(o_dataset.comments, d_dataset["comments"])
        self.assertDictEqual(o_dataset.tags, d_dataset["tags"])
        self.assertDictEqual(
            o_dataset.data_files,
            {
                p_root / "CANTON/CANTON.shx": "CANTON",
                p_root / "CANTON/CANTON.dbf": "CANTON",
                p_root / "CANTON/CANTON.shp": "CANTON",
                p_root / "CANTON/CANTON.cpg": "CANTON",
                p_root / "CANTON/CANTON.prj": "CANTON",
                p_root / "CANTON/sous_dossier/coucou.txt": "CANTON/sous_dossier",
            },
        )
        self.assertEqual(o_dataset.md5_files, [p_root / "CANTON.md5"])
        self.assertTrue(p_md5.exists(), "CANTON.md5 n'existe pas")
        s_data_md5 = p_md5.read_text(encoding="UTF-8")
        for p_file in o_dataset.data_files:
            s_md5 = FileHelper.md5_hash(p_file)
            s_line = f"{s_md5}  data/{p_file.relative_to(p_root)}"
            self.assertIn(s_line, s_data_md5)
