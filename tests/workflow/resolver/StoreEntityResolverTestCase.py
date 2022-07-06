from typing import List
from unittest.mock import patch
from ignf_gpf_api.store.Endpoint import Endpoint

from ignf_gpf_api.store.StoreEntity import StoreEntity
from ignf_gpf_api.store.Upload import Upload

from ignf_gpf_api.workflow.resolver.Errors import NoEntityFoundError, ResolverError
from ignf_gpf_api.workflow.resolver.StoreEntityResolver import StoreEntityResolver

from tests.GpfTestCase import GpfTestCase


class StoreEntityResolverTestCase(GpfTestCase):
    """Tests StoreEntityResolver class.

    cmd : python3 -m unittest -b tests.workflow.resolver.StoreEntityResolverTestCase
    """

    def test_resolve_errors(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve si erreurs."""

        o_store_entity_resolver = StoreEntityResolver("store_entity")

        # Si mot clé incorrect erreur levée
        with self.assertRaises(ResolverError) as o_arc_1:
            o_store_entity_resolver.resolve("other()")
        self.assertEqual(o_arc_1.exception.message, "Erreur du résolveur 'store_entity' avec la chaîne 'other()'.")

        # Si mot clé incorrect erreur levée
        with self.assertRaises(ResolverError) as o_arc_2:
            o_store_entity_resolver.resolve("upload.infos._id [IFO(name=titi)]")
        self.assertEqual(o_arc_2.exception.message, "Erreur du résolveur 'store_entity' avec la chaîne 'upload.infos._id [IFO(name=titi)]'.")

    def test_resolve_no_result(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve si aucun résultat n'est trouvé."""

        o_store_entity_resolver = StoreEntityResolver("store_entity")
        l_uploads: List[StoreEntity] = []

        # On mock la fonction api_list, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(StoreEntity, "api_list", return_value=l_uploads) as o_mock_api_list:
            s_to_solve = "upload.infos._id [INFOS(name=start_%), TAGS(k_tag=v_tag)]"
            with self.assertRaises(NoEntityFoundError) as o_arc:
                o_store_entity_resolver.resolve(s_to_solve)
            # Vérification erreur
            self.assertEqual(o_arc.exception.message, f"Impossible de trouver une entité correspondante (résolveur 'store_entity') avec la chaîne '{s_to_solve}'.")
            # Vérifications o_mock_api_list
            o_mock_api_list.assert_called_once_with(infos_filter={"name": "start_%"}, tags_filter={"k_tag": "v_tag"}, page=1)

    def test_resolve_upload(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un upload."""

        o_store_entity_resolver = StoreEntityResolver("store_entity")
        l_uploads = [
            Upload({"_id": "upload_1", "name": "Name 1", "tags": {"k_tag": "v_tag"}}),
            Upload({"_id": "upload_2", "name": "Name 2", "tags": {"k_tag": "v_tag"}}),
        ]

        # On mock la fonction api_list, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(StoreEntity, "api_list", return_value=l_uploads) as o_mock_api_list:
            s_result = o_store_entity_resolver.resolve("upload.infos._id [INFOS(name=start_%), TAGS(k_tag=v_tag)]")
            # Vérifications o_mock_api_list
            o_mock_api_list.assert_called_once_with(infos_filter={"name": "start_%"}, tags_filter={"k_tag": "v_tag"}, page=1)
            # Vérification id récupérée
            self.assertEqual(s_result, "upload_1")

        # On mock la fonction api_list, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(StoreEntity, "api_list", return_value=l_uploads) as o_mock_api_list:
            s_result = o_store_entity_resolver.resolve("upload.infos.name [INFOS(name=start_%), TAGS(k_tag=v_tag)]")
            # Vérifications o_mock_api_list
            o_mock_api_list.assert_called_once_with(infos_filter={"name": "start_%"}, tags_filter={"k_tag": "v_tag"}, page=1)
            # Vérification name récupérée
            self.assertEqual(s_result, "Name 1")

        # On mock la fonction api_list, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(StoreEntity, "api_list", return_value=l_uploads) as o_mock_api_list:
            s_result = o_store_entity_resolver.resolve("upload.tags.k_tag [INFOS(name=start_%), TAGS(k_tag=v_tag)]")
            # Vérifications o_mock_api_list
            o_mock_api_list.assert_called_once_with(infos_filter={"name": "start_%"}, tags_filter={"k_tag": "v_tag"}, page=1)
            # Vérification name récupérée
            self.assertEqual(s_result, "v_tag")

    def test_resolve_endpoint(self) -> None:
        """Vérifie le bon fonctionnement de la fonction resolve pour un endpoint."""

        o_store_entity_resolver = StoreEntityResolver("store_entity")
        l_uploads = [
            Endpoint({"_id": "endpoint", "name": "Name", "type": "ARCHIVE"}),
        ]

        # On mock la fonction api_list, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(Endpoint, "api_list", return_value=l_uploads) as o_mock_api_list:
            s_result = o_store_entity_resolver.resolve("endpoint.infos._id [INFOS(type=ARCHIVE)]")
            # Vérifications o_mock_api_list
            o_mock_api_list.assert_called_once_with(infos_filter={"type": "ARCHIVE"}, tags_filter={}, page=1)
            # Vérification id récupérée
            self.assertEqual(s_result, "endpoint")

        # On mock la fonction api_list, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(Endpoint, "api_list", return_value=l_uploads) as o_mock_api_list:
            s_result = o_store_entity_resolver.resolve("endpoint.infos.name [INFOS(type=ARCHIVE)]")
            # Vérifications o_mock_api_list
            o_mock_api_list.assert_called_once_with(infos_filter={"type": "ARCHIVE"}, tags_filter={}, page=1)
            # Vérification name récupérée
            self.assertEqual(s_result, "Name")

        # On mock la fonction api_list, on veut vérifier qu'elle est appelée avec les bons param
        with patch.object(Endpoint, "api_list", return_value=l_uploads) as o_mock_api_list:
            s_to_solve = "endpoint.tags.k_tag [INFOS(type=ARCHIVE)]"
            with self.assertRaises(ResolverError) as o_arc:
                o_store_entity_resolver.resolve("endpoint.tags.k_tag [INFOS(type=ARCHIVE)]")
            # Vérification erreur
            self.assertEqual(o_arc.exception.message, f"Erreur du résolveur 'store_entity' avec la chaîne '{s_to_solve}'.")
            # Vérifications o_mock_api_list
            o_mock_api_list.assert_called_once_with(infos_filter={"type": "ARCHIVE"}, tags_filter={}, page=1)
