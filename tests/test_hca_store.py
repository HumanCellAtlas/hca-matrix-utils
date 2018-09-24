import binascii

import hca.dss
import numpy
import pytest
import zarr

import hca_matrix_utils.storage

TEST_DSS_HOST = 'https://dss.integration.data.humancellatlas.org/v1'

TEST_BUNDLES = [
    ["680a9934-63ab-4fc7-a9a9-50ccc332f871",
     "2018-09-20T211624.579399Z",
     "aws",
     {
         "shapes": {
             "cell_id": (1,),
             "cell_metadata": (1, 4),
             "cell_metadata_name": (4,),
             "expression": (1, 58347),
             "gene_id": (58347,),
             "gene_metadata": (0,),
             "gene_metadata_name": (0,),
         },
         "sums": {
             "expression": 1000000,
             "cell_metadata": 10896283,
         },
         "digests": {
             "cell_id": b'11a8effc57c8db3e6247264f1f41e1c80dee00a2',
             "cell_metadata": b'3680e7a6162b9e2afda25ba6fed71d79323bd263',
             "cell_metadata_name": b'feade7edbf56c82df1031039431e667477cc6eba',
             "expression": b'047d15818efb1ebc3de83d7f9ea9d11fe3c3c619',
             "gene_id": b'ff6bc94b0205c5118bdd984c70da5e4f76b84cbc'
         }
     }
    ]
]

@pytest.mark.parametrize("bundle_uuid,version,replica,expected_values", TEST_BUNDLES)
def test_hca_store_read(bundle_uuid, version, replica, expected_values):
    
    client = hca.dss.DSSClient()
    client.host = TEST_DSS_HOST

    hca_store = hca_matrix_utils.storage.HCAStore(client, bundle_uuid, version, replica)
    matrix_root = zarr.group(store=hca_store)

    for dset, expected_shape in expected_values.get("shapes", {}).items():
        assert getattr(matrix_root, dset).shape == expected_shape

    for dset, expected_sum in expected_values.get("sums", {}).items():
        assert numpy.sum(getattr(matrix_root, dset)) == pytest.approx(expected_sum, 1)

    for dset, expected_digest in expected_values.get("digests", {}).items():
        assert binascii.hexlify(getattr(matrix_root, dset).digest()) == expected_digest
