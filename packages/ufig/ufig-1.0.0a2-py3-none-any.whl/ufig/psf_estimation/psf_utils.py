import numpy as np

from ufig import mask_utils

ERR_VAL = 999


def transform_forward(vec, scale):
    vec_transformed = (vec - scale[:, 0]) / scale[:, 1]
    return vec_transformed


def transform_inverse(vec_transformed, scale):
    vec = vec_transformed * scale[:, 1] + scale[:, 0]
    return vec


def position_weights_to_nexp(position_weights):
    n_exp = np.sum(position_weights > 0, axis=1).astype(np.uint16)
    return n_exp


def postprocess_catalog(cat):
    if "psf_flux_ratio_cnn" in cat.dtype.names:
        cat["psf_flux_ratio_cnn"] = np.clip(
            cat["psf_flux_ratio_cnn"], a_min=0.0, a_max=1.0
        )


def get_position_weights(x, y, pointings_maps):
    size_y, size_x = pointings_maps.shape

    x_noedge = x.astype(np.int32)
    y_noedge = y.astype(np.int32)
    x_noedge[x_noedge >= size_x] = size_x - 1
    y_noedge[y_noedge >= size_y] = size_y - 1
    x_noedge[x_noedge < 0] = 0
    y_noedge[y_noedge < 0] = 0

    n_pointings = pointings_maps.attrs["n_pointings"]

    n_bit = 64

    position_weights = mask_utils.decimal_integer_to_binary(
        n_bit, pointings_maps["bit1"][y_noedge, x_noedge], dtype_out=np.float64
    )

    for n in range(2, 6):
        n_pointings -= 64
        if n_pointings > 0:
            position_weights = np.concatenate(
                (
                    position_weights,
                    mask_utils.decimal_integer_to_binary(
                        n_bit,
                        pointings_maps[f"bit{str(n)}"][y_noedge, x_noedge],
                        dtype_out=np.float64,
                    ),
                ),
                axis=1,
                dtype=np.float64,
            )
        else:
            break

    norm = np.sum(np.array(position_weights), axis=1, keepdims=True)
    position_weights /= norm
    position_weights[norm[:, 0] == 0] = 0

    return position_weights
