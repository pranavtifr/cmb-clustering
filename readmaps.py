#! /usr/bin/env python
import astropy.io.fits as pf
import healpy as hp
import numpy as np
def get_maps():
  mapp1 = hp.read_map("../PlanckMaps/HFI_SkyMap_545-100by217-100_2048_R2.02_full_rebeam15lmax4000.fits")
  mapp2 = hp.read_map("../PlanckMaps/HFI_SkyMap_545-100by353-100_2048_R2.02_full_rebeam15lmax4000.fits")
  mapp3 = hp.read_map("../PlanckMaps/HFI_SkyMap_857-100by545-100_2048_R2.02_full_rebeam15lmax4000.fits")
  mapp = np.stack((mapp1,mapp2,mapp3),axis=-1)
  return mapp

def map_cleanup(mapps,min_values,max_values):#Give all the values as arrays
  print(len(mapps))
  print(len(mapps[0]))
  for ite in range(len(mapps)):
    point_source = False
    for i in range(len(mapps[0])):
      if mapps[ite][i] < min_values[i] or mapps[ite][i] > max_values[i]:
      point_source = True
      break

    for i in range(len(mapps[0])):
      if point_source:
      mapps[ite][i] = hp.UNSEEN
  return mapps
