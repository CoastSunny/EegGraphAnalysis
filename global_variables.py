### Loading the data ###
sbj = "IE001_NH"  # Name of the subject
raw_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/'
clean_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/clean/' #folder in which we will save raw cleaned data BEFORE ICA DECOMPOSITION
ica_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/ica/' #folder in which we will save raw data AFTER ICA DECOMPOSITION
epochs_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/epochs/' #folder in which we will save epochs data
result_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/results/'
results_sbj = os.path.join(result_folder, sbj)
raw_fname = sbj + "_RESTINGEC"  # Subject name should be followed by EO or EC
title = 'Subject: ' + raw_fname
raw_file_ext = '.set'
raw_path = os.path.join(raw_folder, raw_fname + raw_file_ext)

### Global Variables ###
n_channels = 128
n_channels_used = 124
bad_color = 'red'
color = dict(eeg='darkblue', eog='purple', stim='yellow')
tmin = 0.0  # exclude the baseline period

#Channels positions
left_temporal = ['E35','E39','E40','E41','E44','E45','E46','E47','E48','E49','E50','E51','E56','E57','E58','E63']
right_temporal = ['E97','E98','E100','E101','E102','E103','E108','E109','E110','E114','E115','E116','E117','E120','E121']
left_parietal = ['E6','E7','E13','E29','E30','E31','E32','E36','E37','E38','E42','E43','E52','E53','E54']
right_parietal = ['E55','E80','E81','E87','E88','E93','E94','E99','E104','E105','E106','E107','E111','E112','E113','E118']
left_occipital = ['E59','E60','E61','E62','E64','E65','E66','E67','E68','E69','E70','E71','E72','E74','E75']
right_occipital = ['E73','E76','E77','E78','E79','E82','E83','E84','E85','E86','E89','E90','E91','E92','E95','E96']
left_frontal = ['E12','E16','E18','E19','E20','E21','E22','E23','E24','E25','E26','E27','E28','E33','E34']
right_frontal = ['E1','E2','E3','E4','E5','E8','E9','E10','E11','E14','E15','E17','E119','E122','E123','E124']
