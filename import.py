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
