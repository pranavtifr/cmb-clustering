#! /usr/bin/env python
"""Do KMeans clustering on CMB Data."""
import numpy as np
import sklearn.cluster as clus
import healpy as hp
import argparse
from readmaps import get_maps, map_cleanup
import skfuzzy as fuzz
# NSIDE = 16
clusters = 13
parser = argparse.ArgumentParser()
parser.add_argument("-N", "--number", help="counter", type=int)
args = parser.parse_args()
COUNTER = args.number
print(COUNTER)
X = get_maps()
print(X.shape)
print("Maps Read")
min_values = [60, 5, 40]
max_values = [200, 30, 100]
X = map_cleanup(X, min_values, max_values)
print("Maps Cleaned")
print(X.shape)
try:
    hp.write_map("clean_map_"+str(COUNTER)+".fits", X[:, 0])
except OSError:
    print("FITS File already existed")
    import _pickle as cPickle
    with open("maap_"+str(COUNTER), 'wb') as fil:
        cPickle.dump(X, fil)
print("Maps Dumped")


def compare_org(clustermethod):
    """
    Use the clustermethod to predict clusters.

    Parameters
    ----------
    clustermethod: Clustering Class from sklearn

    Returns
    -------
    None
        Writes to a the fit to a file

    Raises
    ------
    None

    See Also
    --------
    None

    Notes
    -----
    If the Fits File already exists. It Pickles the predictions.

    """
    pred = clustermethod.fit_predict(X)
    try:
        hp.write_map("agglo_clusters_clean_"
                     + str(COUNTER)+".fits", pred)
    except OSError:
        print("FITS File already existed")
        import _pickle as cPickle
        with open("predkmea_"+str(clusters), 'wb') as fil:
            cPickle.dump(pred, fil)


def fuzzyclus():
    """
    Do Fluzzy Clustering.

    Using skfuzzy

    Parameters
    ----------
    None

    Returns
    -------
    None
        Writes fit to a file

    Raises
    ------
    None

    See Also
    --------
    None

    Notes
    -----
    Pickles the predictions and the u matrix and makes the
    predictions into a map

    """
    import _pickle as cPickle
    for i_clusters in range(10, 50, 1):
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(X.T,
                                                         i_clusters,
                                                         2,
                                                         error=0.005,
                                                         maxiter=1000,
                                                         init=None)
        pred = np.argmax(u, axis=0)
        with open("Ufuz_"+str(i_clusters)+"_fpc_"+str(fpc), 'wb') as fil:
            cPickle.dump(u, fil)
        with open("predfuz_"+str(i_clusters)+"_fpc_"+str(fpc), 'wb') as fil:
            cPickle.dump(pred, fil)
        hp.write_map("clusters_"+str(i_clusters)+"_fpc_"+str(fpc)+".fits",
                     pred)
        print(i_clusters, fpc)


clustermethod = clus.SpectralClustering(n_clusters=clusters)
# clustermethod = clus.AgglomerativeClustering(n_clusters=clusters,
#                                              linkage="ward")
# clustermethod = clus.Birch(n_clusters=clusters)
# clustermethod = clus.AffinityPropagation()
# clustermethod = clus.DBSCAN()
# clustermethod = clus.MiniBatchKMeans(n_clusters=clusters,
#                                    random_state=COUNTER)
compare_org(clustermethod)
# fuzzyclus()
