"""
Created on Thu Feb 25 14:13:40 2021

@author: Spencer Webster-Bass
"""
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# cls = clears the command prompt screen
# pyuic5 -x NuDAS.ui -o gui.py = run this command in the
# same location as the .ui file to create the python
# executable (-x) output  (-o) into a file called gui.py
# pyqt documentation c++ examples: https://doc.qt.io/qtforpython/api.html
# pyqt documentation python examples (archived): https://doc.qt.io/archives/qtforpython-5.12/PySide2/QtWidgets/

# pip install pyqt5: https://pypi.org/project/pyqt5-tools/
#
# how to use venv in python: https://www.geeksforgeeks.org/create-virtual-environment-using-venv-python/

# TODO:
# - better organize your functions
# - decide on if you will store matrices as members, or external npy files, or both
#   - saving matrices to an npy file is done in this class since that is not a gui thing

import os.path
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

# imports added from tkinter
from cov_matrix import cov_matrix
from z_scoring import z_scoring

# assembly_detection
# from python_functions.assembly.assembly_detection import assembly_detection
# import sys
# import os
# sys.path.insert(0, os.path.abspath(r'python_functions\assembly\assembly_detection.py'))
from assembly_detection import assembly_detection


# this class represents the backend of the system
class NuDAS(object):
    def __init__(self):
        self.stimuli_mat = {}
        self.spike_times_dict = {}
        self.spike_binned_mat = {}
        self.sample_period = 24414.0625
        self.sample_rate = 1 / self.sample_period
        self.bin_window = -1

    # the input file contains lists of integers indicating the sample at which
    # a stimulus initiated
    def load_stimulus(self, path):
        # prefixed = [filename for filename in os.listdir(path) if filename.startswith("AudiResp")]
        # path_triggers_dir= 'I:\Parooa\Synapse\i\kiloSorted_DMR\Triggers'
        # filename=find_triggers(path_triggers_dir,path)
        if os.path.exists(path):
            triggers_mat = scipy.io.loadmat(path)
            triggers_mat.pop("__globals__")
            triggers_mat.pop("__header__")
            triggers_mat.pop("__version__")
            print(type(triggers_mat))
            self.stimuli_mat = triggers_mat
            print(self.stimuli_mat)
        else:
            print("Sorry, this folder doesn't exist, try another one")

    def load_spike_times(self, path):
        # path_spikes=path+'/spike_times_good_clust.mat'
        if os.path.exists(path):
            spike_times_raw = scipy.io.loadmat(path)
            # assumes that .mat format will always have the
            # actual data stored in the 3rd idx of the dict
            # or you can remove all of the irrelevant parts of the data
            # like this (but make sure you test it first)...
            # spike_times_mat.pop("__globals__")
            # spike_times_mat.pop("__header__")
            # spike_times_mat.pop("__version__")
            data_key = list(spike_times_raw)[3]
            print(spike_times_raw)
            print(data_key)
            self.spike_times_dict = spike_times_raw[data_key]
            print(self.spike_times_dict)
            print(self.spike_times_dict.shape)
        else:
            print("Sorry, this folder doesn't exist, try another one")

    '''
    bins the spike times matrix
    @:parameter
    time_window (double) : the duration of each bin
    '''
    # Function to return spike_matrix binned at time_window
    def bin_spike_matrix(self, neuron_idx, bin_window, use_idx=False):

        # each key is unfortunately a list of a list
        for k, v in self.spike_times_dict:
            print("key: ", k)
            trial_length = np.amax(v) # in samples
            n = len(v)
            print(n)
            self.spike_binned_mat[k[0][0]] = np.zeros(int(np.ceil(trial_length / bin_window)))
            print(trial_length)
            print(len(self.spike_binned_mat[k[0][0]]))
            # self.spike_binned_mat[k[0][0]][int(np.floor(i / bin_window))] += v[0]
            # print(self.spike_binned_mat[k[0][0]][0])
            for i in range(n):
                # added minus 1 to avoid out of bounds error
                self.spike_binned_mat[k[0][0]][int(np.floor(v[i] / bin_window)) - 1] += 1
            # plt.figure()
            # plt.plot(np.arange(len(self.spike_binned_mat[k[0][0]])), self.spike_binned_mat[k[0][0]])

        # plt.show()

        self.z_scoring()

        return

    def z_scoring(self):
        keys = list(self.spike_binned_mat)
        for k in keys:
            # print(k)
            z_norm_mat = zscore(self.spike_binned_mat[k])
            print(z_norm_mat)

    # -----------------------------------------------------------------------------------
    # TKINTER VERSION OF CLASS METHODS
    # added tkinter functions
    # menu_tkinter.browseFilesTrigger
    def stimulus_to_npy_tk(self, path, dmr=1):
        # prefixed = [filename for filename in os.listdir(path) if filename.startswith("AudiResp")]
        # path_triggers_dir= 'I:\Parooa\Synapse\i\kiloSorted_DMR\Triggers'
        # filename=find_triggers(path_triggers_dir,path)

        if os.path.isfile('./trigger_path.npy'):
            os.remove('trigger_path.npy')

        np.save('trigger_path.npy', path)

    # menu_tkinter.browseFilesNeural
    def spike_times_to_npy_tk(self, path, dmr=1):
        if os.path.isfile('./neural_data_path.npy'):
            os.remove('neural_data_path.npy')
        print(path)
        np.save('neural_data_path.npy', path)

    # Function to load the triggers
    # load_triggers.py
    def load_npy_stimulus_tk(self, path, dmr):
        # prefixed = [filename for filename in os.listdir(path) if filename.startswith("AudiResp")]
        # path_triggers_dir= 'I:\Parooa\Synapse\i\kiloSorted_DMR\Triggers'
        # filename=find_triggers(path_triggers_dir,path)
        if os.path.exists(path):
            trig = scipy.io.loadmat(path)
            if dmr == 1:
                return trig['TrigA'][0], path
            elif dmr == 2:
                return trig['TrigB'][0], path
        else:
            print("Sorry, this folder doesn't exist, try another one")
            return

    # load_spike_times.py
    def load_npy_spike_times_tk(self, path, dmr):
        # path_spikes=path+'/spike_times_good_clust.mat'
        if os.path.exists(path):
            spt_mat = scipy.io.loadmat(path)
            return spt_mat['spikeTimesGoodClust'], path
        else:
            print("Sorry, this folder doesn't exist, try another one")
            return

    # # load_z_norm_mat.py
    # def load_z_norm_mat(self, path, dmr):
    #     # path_spikes=path+'/spike_times_good_clust.mat'
    #     if os.path.exists(path):
    #         spt_mat = scipy.io.loadmat(path)
    #         return spt_mat['spikeTimesGoodClust'], path
    #     else:
    #         print("Sorry, this folder doesn't exist, try another one")
    #         return

    # Function to bin the spikes of cluster cluster_nbr with bin size time_window
    # binning.py
    def binning_tk(self, spt_mat, trig, time_window, cluster_nbr, dmr=1, ftsize=22):
        fs = 24414.0625
        # DMR delimitation (depending on trigger)
        first_t = np.amin(trig) / fs
        last_t = np.amax(trig) / fs

        # Preparing binning,rast_arr has the same duration as the dmr
        N_bins = int((last_t - first_t) / time_window) + 1
        rast_arr = np.zeros(N_bins)

        # Getting cluster numbers
        N_clu = spt_mat.shape[0]
        list_clu = np.zeros(N_clu)

        for clu_ind in range(N_clu):
            list_clu[clu_ind] = spt_mat[clu_ind][0][0][0]

        # Figuring last spikes for cluster of interest
        ind_neuron = np.where(list_clu == cluster_nbr)[0][0]

        ind_last_spike = np.where(spt_mat[ind_neuron][1] / fs <= last_t)[0][-1]
        ind_first_spike = np.where(spt_mat[ind_neuron][1] / fs >= first_t)[0][0]

        # binning
        for t in np.arange(ind_first_spike, ind_last_spike + 1):
            ind_bin = int((spt_mat[ind_neuron][1][t][0] / fs - first_t) / time_window)
            rast_arr[ind_bin] += 1

        return rast_arr[:-1]

    # Function to return spike_matrix binned at time_window
    # spike_matrix.py
    def spike_matrix_tk(self, spt_mat, trig, time_window, cluster_list=None, dmr=1, shuffled=False):
        if cluster_list is not None:
            N_clu_list = len(cluster_list)
        else:
            N_clu_list = spt_mat.shape[0]
        spike_mat = []
        if cluster_list is None:
            for c in range(N_clu_list):
                spike_mat.append(self.binning_tk(spt_mat, trig, time_window, spt_mat[c][0][0][0], dmr))

        else:
            for c in range(N_clu_list):
                spike_mat.append(self.binning_tk(spt_mat, trig, time_window, cluster_list[c], dmr))

        spike_mat = np.array(spike_mat)
        # Shuffle spike_matrix
        if shuffled == True:
            for c in range(N_clu_list):
                perm = np.random.permutation(spike_mat.shape[1])
                spike_mat[c, :] = spike_mat[c, perm]

        return spike_mat

    # menu_tkinter.bin_data(c)
    def bin_data_tk(self, tw):
        # tw=take_user_input_for_something()
        #my_entry = Entry(root)
        #my_entry.pack()
        if not os.path.isfile('./neural_data_path.npy'):
            print('Please open a neural data file first')
        elif not os.path.isfile('./trigger_path.npy'):
            print('Please open a trigger file first')

        else:
            dmr=1
            time_window=tw*0.001
            # CHANGED:
            # neural_data_path=np.load('./neural_data_path.npy',allow_pickle=True)
            neural_data_path=np.load('./neural_data_path.npy',allow_pickle=True)
            neural_data_path=str(neural_data_path)
            print('path:::'+neural_data_path)
            #if neural_data_path[-4:]=='.npy':
                #   neural_data=np.load(neural_data_path,allow_pickle=True)
            spike_times,file_spikes=self.load_npy_spike_times_tk(neural_data_path, dmr)
            #elif neural_data_path[-4:]=='.mat':
            #neural_data=sio.loadmat(neural_data_path)

            trigger_path=np.load('./trigger_path.npy',allow_pickle=True)
            trigger_path=str(trigger_path)


            trig, file_trig = self.load_npy_stimulus_tk(trigger_path,dmr)
            spt_mat = self.spike_matrix_tk(spike_times,trig,time_window,cluster_list=None,dmr=1,shuffled=False)
            spt_mat_1ms = self.spike_matrix_tk(spike_times, trig, 0.001, cluster_list=None, dmr=1, shuffled=False)

            np.save('spike_matrix.npy',spt_mat)
            scipy.io.savemat('./spike_matrix_0.001.mat', mdict={'spt_mat': spt_mat_1ms})

            return spt_mat

    def z_scoring_tk(self, cluster_list=None):

        if not os.path.isfile('./spike_matrix.npy'):
            print("The spike matrix has not been binned")
            return

        spt_mat=np.load('spike_matrix.npy',allow_pickle=True)

        N_clu = spt_mat.shape[0]
        z_norm_mat = zscore(spt_mat, axis=1)
        np.save('z_scored_matrix.npy', z_norm_mat)
        return z_norm_mat

    # correlation is normalized such that all values are inbetween zero and one
    def covariance_matrix(self):
        if not os.path.isfile('./z_scored_matrix.npy'):
            print("In order to perform this operation you must first z-score the data.")
            return None
        z_scored_mat = np.load('./z_scored_matrix.npy', allow_pickle=True)
        cov_mat = np.matmul(z_scored_mat, np.transpose(z_scored_mat))
        cov_mat = cov_mat / z_scored_mat.shape[1]
        np.save('correlation_matrix.npy', cov_mat)
        return cov_mat

    def assembly(self):
        # execute assembly_detection with z_norm_mat as input
        z_norm_mat = np.load('z_scored_matrix.npy')
        sig_eig_vec,bel_lam_min_vec,expl_var = assembly_detection(z_norm_mat)
        np_file = open('neuronal_participation.py')
        exec(np_file.read())
        np_file.close()
        am_file = open('assembly_matching.py')
        exec(am_file.read())
        am_file.close()
        print(type(sig_eig_vec))
        print(sig_eig_vec.shape)
        print(type(bel_lam_min_vec))
        print(bel_lam_min_vec.shape)
        print(type(expl_var))
        print(expl_var.shape)
        return bel_lam_min_vec