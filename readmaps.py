#! /usr/bin/env python
"""Use to read and clean maps."""
import healpy as hp
import numpy as np


def get_maps():
    """
    Read the maps from FITS File.

    Read the maps from different FITS File and then stack it
    columnwise

    Parameters
    ----------
    None

    Returns
    -------
    mapp: Numpy Array
        Returns a map with coordinate having a list of values
    Raises
    ------
    None

    See Also
    --------
    None

    """
    mapp1 = hp.read_map("../PlanckMaps/HFI_SkyMap_545-100by217-100"
                        "_2048_R2.02_full_rebeam15lmax4000.fits")
    mapp2 = hp.read_map("../PlanckMaps/HFI_SkyMap_545-100by353-100"
                        "_2048_R2.02_full_rebeam15lmax4000.fits")
    mapp3 = hp.read_map("../PlanckMaps/HFI_SkyMap_857-100by545-100"
                        "_2048_R2.02_full_rebeam15lmax4000.fits")
    mapp = np.stack((mapp1, mapp2, mapp3), axis=-1)
    return mapp


def map_cleanup(mapps, min_values, max_values):
    """
    Remove the Extreme Values in a Map.

    Remove the Extreme values in the map by using the cutoff
    values given in min_values and max_values.

    Parameters
    ----------
    mapp: Numpy Array
        Map gotten from get_maps()
    min_values: Float Array
    max_values: Float Array
        Each element is the min and max values for the cutoff of the
        corresponding map

    Returns
    -------
    mapp: Numpy Array
        Cleaned Map

    Raises
    ------
    None

    See Also
    --------
    get_maps()

    Notes
    -----
    If the map has values beyond the cutoff all the coordinates are made to
    take the value of hp.UNSEEN

    """
    print(len(mapps))
    print(len(mapps[0]))
    for ite in range(len(mapps)):
        point_source = False
        for i in range(len(mapps[0])):
            if min_values[i] >= max_values[i]:
                raise ValueError("Min value greater than Max Value")
            if mapps[ite][i] < min_values[i] or mapps[ite][i] > max_values[i]:
                point_source = True
                break

        for i in range(len(mapps[0])):
            if point_source:
                mapps[ite][i] = hp.UNSEEN
    return mapps
