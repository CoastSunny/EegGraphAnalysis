#This file contains all the necessary imports
#Mne
import mne
from mne import Epochs
import os
import matplotlib.pyplot as plt
import numpy as np

#Connectivity
from mne.connectivity import spectral_connectivity
from autoreject import get_rejection_threshold

#Networkx
import plotly.plotly as py
from plotly.graph_objs import *
import networkx as nx

#Functions
def is_outlier(points, thresh=3.5):
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh
