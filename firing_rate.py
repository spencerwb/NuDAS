import numpy as np

def firing_rate(spike_mat):
    fir_rate=np.sum(spike_mat,axis=1)
    return fir_rate