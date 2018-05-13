# EEG Graph Analysis
Graph analysis of resting state eeg data using MNE and Networkx

Resting state data are cleaned and a connectivity matrix is created using the phase lag index (PLI).
Then, a graph is built and for unbiased group comparisons an acyclic sub-graph is derived joining all the nodes minimizing edge weights (w = 1/w). This sub-graph is named Minimum spanning tree.
--------------------------------------------------
Preprocessing
- Import the data, filter them (the mne filters already use zero-phase filters) at 1-30Hz.
- Set an average reference.
- Check and exclude bad electrodes before doing ICA.
- Do a first visual inspection of raw data, excluding segments containing obvious artifacts.
- Calculate the rejection thresholds that I will pass to ICA
- Run ICA using the extended-infomax method
- Visual inspect ICA components to check for the ones representing eye-movements or blinks.
- Run an automatic procedure that should highligh those components
- Apply ICA
- Create the epochs and perform a last visual inspection to exclude bad epochs.
- Save the epochs 

Connectivity matrix
- Connectivity matrix calculation using the PLI method.
- Create a graph using those values. Given that I am using a 128-electrodes system, I decided to remove connections of electrodes with a distance below 3cm. That's an arbitrary choice though.
- Plot the connectivity matrix (just for visualization)
- Derive the MST subnetwork (which is actually a maximum spanning tree). It has 124 nodes and 123 edges as I excluded 4 EOG electrodes.
- Plot the adjacency matrix and degree distribution
- Calculation of all the metrics used to characterize MSTs: degree, leaf nodes, leaf fraction , max degree, diameter, eccentricity, betweenness centrality, max betweenness centrality, tree hierarchy and degree correlation.

MST metrics
- PLI index averaged over all the electrodes (I will soon implement average for sub-groups)
- nodes
- edges
- leaf nodes = all the nodes with only 1 edge
- leaf fraction = leaf nodes/nodes 
- max degree in the MST = node with the most edges
- diameter = the longest distance between the distances of any two nodes
- eccentricity
- betweenness centrality
- max betweenness centrality = max value between all the BC values
- Three hierarchy = nx_th = leaf_n/(2 * links * nx_btw_max) [To be checked]
- Degree correlation

----------------------------------------------
Steps for the one subject analysis
0) Global variables: info about the subject
1) Filtering, re-referencing and visual inspection
2) ICA
3) Epoching
4) Connectivity matrix
5) Plots
6) Metrics
7) Saving the results

<img src="https://raw.githubusercontent.com/Davi93/EegGraphAnalysis/master/images/sbj_1.png" height="200" width="200">

-----
- Graph analysis of functional brain networks: practical issues in translational neuroscience; Vellani et al. (2014)
- The trees and the forest: Characterization of complex brain networks with minimum spanning trees; Stam et al. (2014)
-----
