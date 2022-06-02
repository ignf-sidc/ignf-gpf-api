from pathlib import Path
import unittest

from ignf_gpf_api.workflow.resolver.FileResolver import FileResolver


class FileResolverTestCase(unittest.TestCase):
    """Tests FileResolverTestCase class.

    cmd : python3 -m unittest -b tests.workflow.resolver.FileResolverTestCase
    """

    file_path = str(Path(__file__).parent.parent.parent / "_data/action/FileResolver")

    s_str_value: str = "contenu du fichier de type str"
    s_list_value: str = str('["info_1", "info_2"]')
    s_dict_value: str = str('{"k1":"v1", "k2":"v2"}')

    def test_resolve_str(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un str."""
        o_file_resolver = FileResolver("file")
        s_test_str: str = o_file_resolver.resolve(f"str({self.file_path}/text.txt)")
        self.assertEqual(self.s_str_value, s_test_str)

    def test_resolve_list(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un list."""
        o_file_resolver = FileResolver("file")
        s_test_list: str = o_file_resolver.resolve(f"list({self.file_path}/list.json)")
        self.assertEqual(self.s_list_value, s_test_list)

    def test_resolve_dict(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un dict."""
        o_file_resolver = FileResolver("file")
        s_test_dict: str = o_file_resolver.resolve(f"dict({self.file_path}/dict.json)")
        self.assertEqual(self.s_dict_value, s_test_dict)
