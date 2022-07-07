from ignf_gpf_api.workflow.resolver.Errors import ResolveFileInvalidError, ResolveFileNotFoundError, ResolverError
from ignf_gpf_api.workflow.resolver.FileResolver import FileResolver

from tests.GpfTestCase import GpfTestCase


class FileResolverTestCase(GpfTestCase):
    """Tests FileResolver class.

    cmd : python3 -m unittest -b tests.workflow.resolver.FileResolverTestCase
    """

    file_path = GpfTestCase.test_dir_path / "workflow" / "resolver" / "FileResolver"

    s_str_value: str = "contenu du fichier de type str"
    s_list_value: str = str('["info_1", "info_2"]')
    s_dict_value: str = str('{"k1":"v1", "k2":"v2"}')

    def test_resolve_other(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un str."""
        o_file_resolver = FileResolver("file")
        # Si mot clé incorrect erreur levée
        with self.assertRaises(ResolverError) as o_arc_1:
            o_file_resolver.resolve("other(text.txt)")
        self.assertEqual(o_arc_1.exception.message, "Erreur du résolveur 'file' avec la chaîne 'other(text.txt)'.")

    def test_resolve_str(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un str."""
        o_file_resolver = FileResolver("file")
        # Si ok
        s_test_str: str = o_file_resolver.resolve(f"str({self.file_path}/text.txt)")
        self.assertEqual(self.s_str_value, s_test_str)
        # Si non existant erreur levée
        with self.assertRaises(ResolveFileNotFoundError) as o_arc_1:
            o_file_resolver.resolve("str(not-existing.txt)")
        self.assertEqual(o_arc_1.exception.message, "Erreur de traitement d'un fichier (résolveur 'file') avec la chaîne 'str(not-existing.txt)': fichier non existant.")

    def test_resolve_list(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un list."""
        o_file_resolver = FileResolver("file")
        # Si ok
        s_test_list: str = o_file_resolver.resolve(f"list({self.file_path}/list.json)")
        self.assertEqual(self.s_list_value, s_test_list)
        # Si non existant erreur levée
        with self.assertRaises(ResolveFileNotFoundError) as o_arc_1:
            o_file_resolver.resolve("list(not-existing.json)")
        self.assertEqual(o_arc_1.exception.message, "Erreur de traitement d'un fichier (résolveur 'file') avec la chaîne 'list(not-existing.json)': fichier non existant.")
        # Si pas liste erreur levée
        with self.assertRaises(ResolveFileInvalidError) as o_arc_2:
            o_file_resolver.resolve(f"list({self.file_path}/dict.json)")
        self.assertEqual(o_arc_2.exception.message, f"Erreur de traitement d'un fichier (résolveur 'file') avec la chaîne 'list({self.file_path}/dict.json)'.")
        # Si pas valide erreur levée
        with self.assertRaises(ResolveFileInvalidError) as o_arc_3:
            o_file_resolver.resolve(f"list({self.file_path}/not-valid.json)")
        self.assertEqual(o_arc_3.exception.message, f"Erreur de traitement d'un fichier (résolveur 'file') avec la chaîne 'list({self.file_path}/not-valid.json)'.")

    def test_resolve_dict(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un dict."""
        o_file_resolver = FileResolver("file")
        # Si ok
        s_test_dict: str = o_file_resolver.resolve(f"dict({self.file_path}/dict.json)")
        self.assertEqual(self.s_dict_value, s_test_dict)
        # Si non existant erreur levée
        with self.assertRaises(ResolveFileNotFoundError) as o_arc_1:
            o_file_resolver.resolve("dict(not-existing.json)")
        self.assertEqual(o_arc_1.exception.message, "Erreur de traitement d'un fichier (résolveur 'file') avec la chaîne 'dict(not-existing.json)': fichier non existant.")
        # Si pas liste erreur levée
        with self.assertRaises(ResolveFileInvalidError) as o_arc_2:
            o_file_resolver.resolve(f"dict({self.file_path}/list.json)")
        self.assertEqual(o_arc_2.exception.message, f"Erreur de traitement d'un fichier (résolveur 'file') avec la chaîne 'dict({self.file_path}/list.json)'.")
        # Si pas valide erreur levée
        with self.assertRaises(ResolveFileInvalidError) as o_arc_3:
            o_file_resolver.resolve(f"dict({self.file_path}/not-valid.json)")
        self.assertEqual(o_arc_3.exception.message, f"Erreur de traitement d'un fichier (résolveur 'file') avec la chaîne 'dict({self.file_path}/not-valid.json)'.")
