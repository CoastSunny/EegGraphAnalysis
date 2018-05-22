# Connectivity strength analysis
#We create a mask to remove the diagonal from the Count (which is self-correlation)
mask = np.ones((n_channels_used,n_channels_used))
mask =  (mask-np.diag(np.ones(n_channels_used))).astype(np.bool)

r_con = con + con.T - np.diag(np.diag(con)) #I reflect the matrix to correctly calculate all the connectivity strength values
mean_connectivity = round(np.mean(r_con[mask]),4) #Whole mean connectivity strength

#Alternative
r_con[r_con == 0] = np.nan
mean_connectivity = np.nanmean(r_con)
#THIS HAS TO BE DONE AFTER THE CALCULATION OF THE WHOLE CONNECTIVITY MATRIX
# Connectivity strength in a sub-avareage of electrodes (frontal, occipital, temporal and parietal)
lt_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_temporal) #left_temporal electrodes and so forth
rt_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=right_temporal)
lp_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_parietal)
rp_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=right_parietal)
lo_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_occipital)
ro_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=right_occipital)
lf_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_frontal)
rf_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=right_frontal)

#Now we consider left and right together, joining the each couple of arrays
t_picks = np.append(lt_picks,rt_picks) #temporal
f_picks = np.append(lf_picks,rf_picks) #frontal
o_picks = np.append(lo_picks,ro_picks) #occipital
p_picks = np.append(lp_picks,rp_picks) #parietal

#Connectivity strength for temporal electrodes
t_con = r_con[t_picks][:, t_picks]
t_con_mean = round(np.nanmean(t_con),4)
#Connectivity strength for frontal electrodes
f_con = r_con[f_picks][:, f_picks]
f_con_mean = round(np.nanmean(f_con),4)
#Connectivity strength for occipital electrodes
o_con = r_con[o_picks][:, o_picks]
o_con_mean = round(np.nanmean(o_con),4)
#Connectivity strength for parietal electrodes
p_con = r_con[p_picks][:, p_picks]
p_con_mean = round(np.nanmean(p_con),4)

#Now we consider left/right electrodes, we will therefore have 8 different means
#Left/right temporal electrodes
#Left temporal
lt_con = r_con[lt_picks][:, lt_picks]
lt_con_mean = round(np.nanmean(lt_con),4)
#right temporal
rt_con = r_con[rt_picks][:, rt_picks]
rt_con_mean = round(np.nanmean(rt_con),4)

#Left/right frontal electrodes
#Left frontal
lf_con = r_con[lf_picks][:, lf_picks]
lf_con_mean = round(np.nanmean(lf_con),4)
#right frontal
rf_con = r_con[rf_picks][:, rf_picks]
rf_con_mean = round(np.nanmean(rf_con),4)

#Left/right parietal electrodes
#Left parietal
lp_con = r_con[lp_picks][:, lp_picks]
lp_con_mean = round(np.nanmean(lp_con),4)
#right parietal
rp_con = r_con[rp_picks][:, rp_picks]
rp_con_mean = round(np.nanmean(rp_con),4)

#Left/right occipital electrodes
#Left occipital
lo_con = r_con[lo_picks][:, lo_picks]
lo_con_mean = round(np.nanmean(lo_con),4)
#right occipital
ro_con = r_con[ro_picks][:, ro_picks]
ro_con_mean = round(np.nanmean(ro_con),4)


#Plotting the data
import matplotlib.pyplot as plt
import plotly.plotly as py
#Here we plot the general mean connectivities of the four groups
y = [f_con_mean,t_con_mean,p_con_mean,o_con_mean]
N = len(y)
x = ['frontal','temporal','parietal','occipital']
width = 1/1.5
plt.bar(x, y, width, color="darkgrey")
plt.show()

#Now we plot them considering lef/right (to be implemented, just copy the previous code and adapt it)
