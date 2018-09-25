import binascii

import hca.dss
import numpy
import pytest
import zarr

import hca_matrix_utils.storage

import bundles

TEST_DSS_HOST = 'https://dss.integration.data.humancellatlas.org/v1'


@pytest.mark.parametrize("bundle_spec", bundles.test_bundles)
def test_hca_store_read(bundle_spec):
    """Test using the HCAStore with zarr."""

    bundle_uuid = bundle_spec["uuid"]
    bundle_version = bundle_spec["version"]
    replica = bundle_spec["replica"]
    expected_values = bundle_spec["description"]
    
    client = hca.dss.DSSClient()
    client.host = TEST_DSS_HOST

    hca_store = hca_matrix_utils.storage.HCAStore(client, bundle_uuid, bundle_version, replica)
    matrix_root = zarr.group(store=hca_store)

    for dset, expected_shape in expected_values.get("shapes", {}).items():
        assert getattr(matrix_root, dset).shape == expected_shape

    for dset, expected_sum in expected_values.get("sums", {}).items():
        assert numpy.sum(getattr(matrix_root, dset)) == pytest.approx(expected_sum, 1)

    for dset, expected_digest in expected_values.get("digests", {}).items():
        assert binascii.hexlify(getattr(matrix_root, dset).digest()) == expected_digest
