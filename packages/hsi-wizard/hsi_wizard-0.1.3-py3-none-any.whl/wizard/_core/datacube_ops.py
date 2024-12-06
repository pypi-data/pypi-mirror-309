"""
_core/datacube_ops.py
=====================

.. module:: datacube_ops
    :platform: Unix
    :synopsis: DataCube Operations.

Module Overview
---------------

This module contains functions for processing and manipulating `DataCube` instances, including
operations like removing spikes, resizing cubes, and merging cubes or wavelengths.

Functions
---------

.. autofunction:: remove_spikes
.. autofunction:: resize

"""

import cv2
import numpy as np
from joblib import Parallel, delayed

from . import DataCube

from .._processing.spectral import calculate_modified_z_score, spec_baseline_als


def _process_slice(spec_out_flat, spikes_flat, idx, window):
    """
    Process a single slice of the data cube to remove spikes by replacing them with the mean
    of neighboring values within a given window.

    Parameters
    ----------
    spec_out_flat : numpy.ndarray
        Flattened output spectrum data from the data cube.
    spikes_flat : numpy.ndarray
        Flattened boolean array indicating where spikes are detected in the cube.
    idx : int
        Index of the current slice to process.
    window : int
        The size of the window used to calculate the mean of neighboring values.

    Returns
    -------
    tuple
        A tuple containing the index of the processed slice and the modified spectrum slice.
    """

    w_h = int(window / 2)
    spike = spikes_flat[idx]
    tmp = np.copy(spec_out_flat[idx])

    for spk_idx in np.where(spike)[0]:
        window_min = max(0, spk_idx - w_h)
        window_max = min(len(tmp), spk_idx + w_h + 1)

        if window_min == spk_idx:
            window_data = tmp[spk_idx + 1:window_max]
        elif window_max == spk_idx + 1:
            window_data = tmp[window_min:spk_idx]
        else:
            window_data = np.concatenate((tmp[window_min:spk_idx], tmp[spk_idx + 1:window_max]))

        if len(window_data) > 0:
            tmp[spk_idx] = np.mean(window_data)

    return idx, tmp


def remove_spikes(dc, threshold: int = 6500, window: int = 3):
    """
    Remove cosmic spikes from the data cube based on a z-score threshold and a smoothing window.

    This function identifies spikes using the modified z-score and replaces the detected spikes
    with the mean of neighboring values within the specified window.

    Parameters
    ----------
    dc : DataCube
        The input `DataCube` from which cosmic spikes are to be removed.
    threshold : int, optional
        The threshold value for detecting spikes based on the modified z-score. Default is 6500.
    window : int, optional
        The size of the window used to calculate the mean of neighboring values
        when replacing spikes. Default is 3.

    Returns
    -------
    DataCube
        The `DataCube` with spikes removed.
    """

    z_spectrum = calculate_modified_z_score(dc.cube)
    spikes = abs(z_spectrum) > threshold
    cube_out = dc.cube.copy()

    spikes_flat = spikes.reshape(dc.cube.shape[0], -1)
    spec_out_flat = cube_out.reshape(cube_out.shape[0], -1)

    results = Parallel(n_jobs=-1)(
        delayed(_process_slice)(spec_out_flat, spikes_flat, idx, window) for idx in range(spikes_flat.shape[0]))

    for idx, tmp in results:
        spec_out_flat[idx] = tmp

    dc.set_cube(spec_out_flat.reshape(cube_out.shape))
    return dc


def resize(dc, x_new: int, y_new: int, interpolation: str = 'linear') -> None:
    """
    Resize the data cube to new x and y dimensions using the specified interpolation method.

    This function resizes each 2D slice (x, y) of the data cube according to the provided dimensions
    and interpolation method.

    Interpolation methods:
    - `linear`: Bilinear interpolation (ideal for enlarging).
    - `nearest`: Nearest neighbor interpolation (fast but blocky).
    - `area`: Pixel area interpolation (ideal for downscaling).
    - `cubic`: Bicubic interpolation (high quality, slower).
    - `lanczos`: Lanczos interpolation (highest quality, slowest).

    Parameters
    ----------
    dc : DataCube
        The `DataCube` instance to be resized.
    x_new : int
        The new width (x-dimension) of the data cube.
    y_new : int
        The new height (y-dimension) of the data cube.
    interpolation : str, optional
        The interpolation method to use for resizing. Default is 'linear'.

    Raises
    ------
    ValueError
        If the specified interpolation method is not recognized.

    Returns
    -------
    None
        The function modifies the `DataCube` in-place.
    """

    mode = None

    # Some Warning ;)
    if dc.shape[1] > x_new:
        print('\033[93mx_new is smaller than the existing cube, you will lose information\033[0m')

    if dc.shape[2] > y_new:
        print('\033[93my_new is smaller than the existing cube, you will lose information\033[0m')

    # choose interpolation mode
    if interpolation == 'linear':
        mode = cv2.INTER_LINEAR
    elif interpolation == 'nearest':
        mode = cv2.INTER_NEAREST
    elif interpolation == 'area':
        mode = cv2.INTER_AREA
    elif interpolation == 'cubic':
        mode = cv2.INTER_CUBIC
    elif interpolation == 'lanczos':
        mode = cv2.INTER_LANCZOS4
    else:
        raise ValueError(f'Interpolation method `{interpolation}` not recognized.')

    # loop over layers
    _cube = np.empty(shape=(dc.shape[0], x_new, y_new))
    for idx, layer in enumerate(dc.cube):
        _cube[idx] = cv2.resize(layer, (y_new, x_new), interpolation=mode)

    # set cube and update shape
    dc.set_cube(_cube)


def baseline_als(dc: DataCube = None, lam: float = 1000000, p: float = 0.01, niter: int = 10) -> DataCube:
    """

    :param dc:
    :param lam:
    :param p:
    :param niter:
    :return:
    """
    for x in range(dc.shape[1]):
        for y in range(dc.shape[2]):
            dc.cube[:, x, y] -= spec_baseline_als(
                spectrum=dc.cube[:, x, y],
                lam=lam,
                p=p,
                niter=niter
            )
    return dc
