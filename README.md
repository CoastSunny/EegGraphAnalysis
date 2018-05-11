# EEG Graph Analysis
Graph analysis of resting state eeg data using MNE and Networkx

Resting state data are cleaned and a connectivity matrix is created using the phase lag index (PLI).
Then, a graph is built and described using classical measures. For unbiased group comparisons an acyclic sub-graph is created joining all the nodes minimizing edge weights (w = 1/w). This sub-graph is named Minimum spanning tree.



<img src="https://raw.githubusercontent.com/Davi93/EegGraphAnalysis/master/images/sbj_1.png" height="200" width="200">
<img src="https://raw.githubusercontent.com/Davi93/EegGraphAnalysis/master/images/sbj_2.png" height="200" width="200">


-----
- Graph analysis of functional brain networks: practical issues in translational neuroscience; Vellani et al. (2014)
- The trees and the forest: Characterization of complex brain networks with minimum spanning trees; Stam et al. (2014)
-----

Steps for the one subject analysis
0) Global variables: info about the subject
1) Filtering, re-referencing and visual inspection
2) ICA
3) Epoching
4) Connectivity matrix
5) Plots
6) Metrics
7) Saving the results
