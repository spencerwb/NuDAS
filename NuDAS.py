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
# pyqt documentation: https://doc.qt.io/qtforpython/api.html

# pyqt5 https://pypi.org/project/pyqt5-tools/
#
# how to use venv in python: https://www.geeksforgeeks.org/create-virtual-environment-using-venv-python/

import os.path
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


# this class represents the backend of the system
class NuDAS(object):
    def __init__(self):
        self.stimuli_mat = {}
        self.spike_times_dict = {}
        self.spike_binned_mat = {}
        self.sample_period = 24414.0625
        self.sample_rate = 1 / self.sample_period

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
            plt.figure()
            plt.plot(np.arange(len(self.spike_binned_mat[k[0][0]])), self.spike_binned_mat[k[0][0]])

        plt.show()

        self.z_scoring()

        return

    def z_scoring(self):
        for k, v in self.spike_binned_mat:
            print(k[0][0])
            z_norm_mat = zscore(v)
            print(z_norm_mat)

    def cov_mat(self, z_norm_mat):
        cov_mat = np.matmul(z_norm_mat, np.transpose(z_norm_mat))
        cov_mat = cov_mat / z_norm_mat.shape[1]
        return cov_mat





# def window():
#     app = QApplication(sys.argv)
#     win = QMainWindow()
#     # top left hand corner
#     xpos = 200
#     ypos = 200
#     width = 300
#     height = 300
#     win.setGeometry(xpos, ypos, width, height)
#     win.setWindowTitle("NuDAS")
#
#     win.show()
#     sys.exit(app.exec_())
#
#
# # importing data
# p = "../spike_times_good_clust.mat"
# # p = input("enter file location for spike times: ")
# spike, p2 = load_spike_times(p)
# # print(spike[0])
# # print(spike[0][1])
# # print(spike[0][1][0])

# # ../AudiResp_24_24-190414-163146-ripplesF_triggers.mat
# # p = input("enter file location for triggers/stimulus files: ")
# p = "../AudiResp_24_24-190414-163146-ripplesF_triggers.mat"
# p = r"C:\Users\webst\OneDrive\academic\2020-21 SEN\2nd_semester\cis_497\auditory_populations_project\AudiResp_24_24-190414-163146-ripplesF_triggers.mat"
# nudas = NuDAS()
# nudas.load_stimulus(p)
# # trigs, p2 = load_triggers(p)
#
# # preprocessing
# # binning
# r = binning()
#
# window()
