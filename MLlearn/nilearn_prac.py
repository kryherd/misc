#!/usr/bin/env python

from nilearn import plotting
import numpy as np
import os
import nibabel as nib
import matplotlib.pyplot as plt

### View basic images
# point to dataset
aud = "./Data/audio_contrast.nii"
plotting.plot_img(aud)

vis = "./Data/visual_contrast.nii"
plotting.plot_img(vis)

### Smoothing
from nilearn import image
smooth_aud_img = image.smooth_img(aud, fwhm=10) # in-memory object
print(smooth_aud_img)
plotting.plot_img(smooth_aud_img)
plotting.show() #required outside of ipython

smooth_aud_img.to_filename('smooth_aud_img.nii.gz')

### Visualizing a 3D file
bg = "./Data/TT_N27.nii"
plotting.plot_stat_map(aud, bg) #no threshold
plotting.plot_stat_map(aud, bg, threshold=3)
plotting.plot_stat_map(vis, bg, threshold=3)

### Visualizing a 4D file
rsn = datasets.fetch_atlas_smith_2009()['rsn10']
print(rsn)
print(image.load_img(rsn).shape)
first_rsn = image.index_img(rsn, 0)
print(first_rsn.shape)
plotting.plot_stat_map(first_rsn)



for img in image.iter_img(rsn):
    # img is now an in-memory 3D img
    plotting.plot_stat_map(img, threshold=3, display_mode="z", cut_coords=1,
                           colorbar=False)
#### fMRI Decoding

# load epi data
fmri_filename = nib.load("./Data/epi.nii")

# look at mask
mask_filename = "./Data/mask.nii"
plotting.plot_roi(mask_filename, bg_img="./Data/anat_strip.nii",
                 cmap='Paired')

# use the masker to mask the fMRI data

from nilearn.input_data import NiftiMasker
masker = NiftiMasker(mask_img=mask_filename, standardize=True)

# We give the masker a filename and retrieve a 2D array ready
# for machine learning with scikit-learn
fmri_masked = masker.fit_transform(fmri_filename)





