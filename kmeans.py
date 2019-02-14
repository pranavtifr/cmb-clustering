#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import *
from sklearn.datasets import make_blobs
import healpy as hp
from readmaps import *
import skfuzzy as fuzz
#NSIDE = 16
features = 50
clusters = 20
#X, y = make_blobs(n_samples=hp.nside2npix(NSIDE), n_features=features, centers=features)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-N","--number",help="counter",type=int)
args = parser.parse_args()
COUNTER = args.number
print(COUNTER)
X = get_maps()
# Initializing Cluster Method
def compare_org(clustermethod):
  pred = clustermethod.fit_predict(X)
  #import _pickle as cPickle
  #with open("predkmea_"+str(clusters),'wb') as fil:
    #cPickle.dump(pred,fil)
  hp.write_map("clusters_"+str(COUNTER)+".fits",pred)

def fuzzyclus():
  for i_clusters in range(10,50,1):
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(X.T, i_clusters, 2, error=0.005, maxiter=1000, init=None)
    pred =  np.argmax(u, axis=0)
    import _pickle as cPickle
    with open("Ufuz_"+str(i_clusters)+"_fpc_"+str(fpc),'wb') as fil:
      cPickle.dump(u,fil)
    with open("predfuz_"+str(i_clusters)+"_fpc_"+str(fpc),'wb') as fil:
      cPickle.dump(pred,fil)
    hp.write_map("clusters_"+str(i_clusters)+"_fpc_"+str(fpc)+".fits",pred)
    print(i_clusters,fpc)

#clustermethod = AgglomerativeClustering(n_clusters=clusters,linkage="ward")
#compare_org(clustermethod)
#clustermethod = AffinityPropagation()
#compare_org(clustermethod)
#clustermethod = DBSCAN()
#compare_org(clustermethod)
clustermethod = MiniBatchKMeans(n_clusters=clusters)
compare_org(clustermethod)
#fuzzyclus()
