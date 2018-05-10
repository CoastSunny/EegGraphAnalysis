#Firstly we load the cleaned data
#cleaned_file = os.path.join(clean_folder, raw_fname + '.fif')
#raw = mne.io.read_raw_fif(cleaned_file, preload = True)

# We load the epochs
epochs mne.io.read_raw_fif(cleaned_file, preload = True)
