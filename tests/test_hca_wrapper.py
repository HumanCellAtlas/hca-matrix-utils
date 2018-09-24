import numpy
import pytest

import hca_matrix_utils.wrappers

import bundles

@pytest.mark.parametrize("bundle_spec", bundles.test_bundles)
def test_hca_wrapper_pandas(bundle_spec):
    """Test the HCA matrix wrapper"""

    bundle_uuid = bundle_spec["uuid"]
    bundle_version = bundle_spec["version"]

    hca_mat = hca_matrix_utils.wrappers.HCAExpressionMatrix(
        bundle_uuid=bundle_uuid,
        bundle_version=bundle_version
    )

    exp_df, meta_df = hca_mat.to_pandas()
    
    assert numpy.sum(exp_df.values) == pytest.approx(bundle_spec["description"]["sums"]["expression"], 1)
    assert numpy.sum(meta_df.values) == pytest.approx(bundle_spec["description"]["sums"]["cell_metadata"], 1)
