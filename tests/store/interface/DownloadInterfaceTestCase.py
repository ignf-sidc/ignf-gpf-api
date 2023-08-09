from pathlib import Path
from unittest.mock import mock_open, patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.store.interface.DownloadInterface import DownloadInterface
from tests.GpfTestCase import GpfTestCase


class DownloadInterfaceTestCase(GpfTestCase):
    """Tests DownloadInterface class.

    cmd : python3 -m unittest -b tests.store.interface.DownloadInterfaceTestCase
    """

    def test_api_download(self) -> None:
        """Vérifie le bon fonctionnement de api_download."""
        p_file = Path("rep/output.txt")
        o_response = GpfTestCase.get_response(content=b"contenu du fichier")
        for s_datastore in [None, "api_download"]:
            # On mock la fonction route_request, on veut vérifier qu'elle est appelée avec les bons param
            with patch.object(ApiRequester, "route_request", return_value=o_response) as o_mock_request:
                o_opener = mock_open()
                with patch.object(Path, "open", return_value=o_opener.return_value) as o_mock_open:
                    # On effectue l ajout d'un commentaire
                    # On instancie une entité à qui on va ajouter un commentaire
                    o_download_interface = DownloadInterface({"_id": "id_entité"}, s_datastore)
                    # On appelle la fonction api_download
                    o_download_interface.api_download(p_file)
                    # Vérification sur o_mock_request
                    o_mock_request.assert_called_once_with(
                        "store_entity_download",
                        route_params={"store_entity": "id_entité", "datastore": s_datastore},
                    )
                    o_mock_open.assert_called_once_with("wb", encoding="UTF-8")
                    o_opener.return_value.write.assert_called_once()
