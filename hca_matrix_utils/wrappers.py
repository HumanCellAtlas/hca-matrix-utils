# -*- coding: utf-8 -*-
"""Wrapper class around HCA expression matrices that provide some useful methods."""

import hca.dss
import zarr

import hca_matrix_utils.storage


class HCAExpressionMatrix(object):

    """
    Interface to an expression matrix in an HCA bundle.

    Parameters
    ----------

    bundle_uuid : str
        DCP uuid of the analysis bundle.
    bundle_version : str, optional
        DCP version of the analysis bundle. (default is None, which means use
        the latest version of the bundle)
    replica : str, optional
        Replica of the DCP from which to access data. (default is "aws")
    dss_instance : str, optional
        Which instance of the DCP data storage system to use. (default is None, which means
        use the default value from hca.dss.DSSClient; other valid values are "integration",
        "staging", "dev"


    Methods
    -------
    to_pandas(concat=False)
        Get a pandas dataframe of the expression matrix

    """

    def __init__(self, bundle_uuid, bundle_version=None, replica="aws", dss_instance=None):

        dss_client = self._get_client(dss_instance)

        zarr_store = hca_matrix_utils.storage.HCAStore(
            dss_client=dss_client,
            bundle_uuid=bundle_uuid,
            bundle_version=bundle_version,
            replica=replica)

        self._matrix_root = zarr.group(store=zarr_store)

    @staticmethod
    def _get_client(dss_instance):
        client = hca.dss.DSSClient()
        if not dss_instance:
            client.host = "https://dss.integration.data.humancellatlas.org/v1"
        else:
            client.host = "https://dss.{dss_instance}.data.humancellatlas.org/v1".format(
                dss_instance=dss_instance)
        return client

    def to_pandas(self, concat=False):
        """Get a pandas dataframe of the expression matrix

        Parameters
        ----------
        concat : bool, optional
            Concatenate the expression and cell metadata into a single dataframe
            (default is False)

        Returns
        -------
        pandas.DataFrame or list of pandas.DataFrame
            DataFrame(s) with expression and metadata values

        """

        import pandas as pd

        exp_df = pd.DataFrame(
            data=self._matrix_root.expression[:],
            index=self._matrix_root.cell_id[:],
            columns=self._matrix_root.gene_id[:])
        cell_metadata_df = pd.DataFrame(
            data=self._matrix_root.cell_metadata[:],
            index=self._matrix_root.cell_id[:],
            columns=self._matrix_root.cell_metadata_name[:])

        if concat:
            return pd.concat([exp_df, cell_metadata_df], axis=1, copy=False)

        return exp_df, cell_metadata_df
