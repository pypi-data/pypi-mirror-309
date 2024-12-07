import h5py
import numpy as np
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import logger

from ufig.psf_estimation import psf_utils
from ufig.psf_estimation.tiled_regressor import (
    TiledRobustPolynomialRegressor as Regressor,
)

LOGGER = logger.get_logger(__file__)


def predict_psf(position_xy, position_weights, regressor, settings, n_per_chunk=1000):
    position_xy_transformed = psf_utils.transform_forward(
        position_xy, scale=settings["scale_pos"]
    )
    position_xy_transformed_weights = np.concatenate(
        [position_xy_transformed, position_weights], axis=1
    )
    position_par_post = regressor.predict(
        position_xy_transformed_weights, batch_size=n_per_chunk
    )
    position_par_post[:] = psf_utils.transform_inverse(
        position_par_post, settings["scale_par"]
    )
    select_no_coverage = (position_weights.sum(axis=1) == 0) | np.any(
        ~np.isfinite(position_par_post), axis=1
    )
    position_par_post[select_no_coverage] = 0

    return position_par_post, select_no_coverage


def predict_psf_with_file(position_xy, filepath_psfmodel, id_pointing="all"):
    if position_xy.shape[1] != 2:
        raise ValueError(
            f"Invalid position_xy shape (should be n_obj x 2) {position_xy.shape}"
        )

    # Setup interpolator
    with h5py.File(filepath_psfmodel, "r") as fh5:
        par_names = at.set_loading_dtypes(fh5["par_names"][...])
        # n_psf_dim = len(par_names)
        pointings_maps = fh5["map_pointings"]
        # n_pointings = pointings_maps.attrs['n_pointings']
        position_weights = psf_utils.get_position_weights(
            position_xy[:, 0], position_xy[:, 1], pointings_maps
        )
        poly_coeffs = fh5["arr_pointings_polycoeffs"][...]
        unseen_pointings = fh5["unseen_pointings"][...]
        settings = {
            key: at.set_loading_dtypes(fh5["settings"][key][...])
            for key in fh5["settings"]
        }
        # set_unseen_to_mean = bool(fh5['set_unseen_to_mean'][...])
        settings.setdefault("polynomial_type", "standard")
        LOGGER.debug("polynomial_type={}".format(settings["polynomial_type"]))

    regressor = Regressor(
        poly_order=settings["poly_order"],
        ridge_alpha=settings["ridge_alpha"],
        polynomial_type=settings["polynomial_type"],
        poly_coefficients=poly_coeffs,
        unseen_pointings=unseen_pointings,
    )

    if id_pointing == "all":
        LOGGER.info(
            f"prediction for cnn models n_pos={position_xy.shape[0]} id_pointing=all"
        )

        position_par_post, select_no_coverage = predict_psf(
            position_xy, position_weights, regressor, settings
        )

        position_par_post = np.core.records.fromarrays(
            position_par_post.T, names=",".join(par_names)
        )
        psf_utils.postprocess_catalog(position_par_post)
        n_exposures = psf_utils.position_weights_to_nexp(position_weights)

        yield position_par_post, select_no_coverage, n_exposures

    else:
        raise NotImplementedError(
            "This feature is not yet implemented due to the polynomial coefficients"
            " covariances which are a tiny bit tricky but definitely doable"
        )
