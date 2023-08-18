from pathlib import Path
from typing import List, Dict, Any
from unittest.mock import patch

from ignf_gpf_api.io.ApiRequester import ApiRequester
from ignf_gpf_api.io.Config import Config
from ignf_gpf_api.store.Errors import StoreEntityError
from ignf_gpf_api.store.interface.CreatedByUploadFileInterface import CreatedByUploadFileInterface
from tests.GpfTestCase import GpfTestCase

# pylint:disable=protected-access


class CreatedByUploadFileInterfaceTestCase(GpfTestCase):
    """Tests CreatedByUploadFileInterface class.

    cmd : python3 -m unittest -b tests.store.interface.CreatedByUploadFileInterfaceTestCase
    """

    def test_api_create(self) -> None:
        "Vérifie le bon fonctionnement de api_create."
        p_file = Path("rep/file")
        s_api_path = "path/dans_api"
        d_res_data = {"base": "data"}
        s_key_file = "file"
        d_data = {**d_res_data, "file": p_file, "api_path": s_api_path}
        o_response = self.get_response(json={"_id": "123456789"})

        for s_datastore in [None, "api_create"]:
            d_route_params = {"datastore": s_datastore} if s_datastore else None

            # On mock la fonction route_upload_file, on veut vérifier qu'elle est appelée avec les bons param
            with patch.object(ApiRequester, "route_upload_file", return_value=o_response) as o_mock_request:
                # mock de Config.get_str()
                with patch.object(Config, "get_str", return_value=s_key_file) as o_mock_config:

                    # On appelle la fonction api_create
                    o_entity = CreatedByUploadFileInterface.api_create({**d_data}, d_route_params)

                    # vérifications
                    o_mock_request.assert_called_once_with(
                        "store_entity_upload",
                        p_file,
                        s_key_file,
                        route_params=d_route_params,
                        params={"path": s_api_path},
                        method=ApiRequester.POST,
                        data=d_res_data,
                    )
                    o_mock_config.assert_any_call("store_entity", "create_file_key")
                    self.assertIsInstance(o_entity, CreatedByUploadFileInterface)
                    self.assertEqual(o_entity.id, "123456789")
                    self.assertEqual(o_entity.datastore, s_datastore)

        # problème de paramétrage :
        s_message = 'Entité créée par l\'upload d\'un fichier, les clefs "file": Path("chemin fichier") et "api_path": "nom fichier" sont obligatoires dans data'

        l_data: List[Dict[str, Any]] = [{}, {"file": p_file}, {"api_path": s_api_path}]
        for d_data in l_data:
            with self.assertRaises(StoreEntityError) as o_arc:
                CreatedByUploadFileInterface.api_create(d_data, d_route_params)
            self.assertEqual(o_arc.exception.message, s_message)
