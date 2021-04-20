import numpy as np
from itertools import permutations

# Match PCA assemblies with ICA assemblies to facilitate comparison. Distance used: absolute
def assembly_matching(sig_eig_vec,rot_seg):
    d_max_pca=np.argmax(abs(sig_eig_vec),axis=1)
    d_max_ica=np.argmax(abs(rot_seg),axis=1)
    perms = []
    diff=[]
    for perm in permutations(range(sig_eig_vec.shape[0])):
        perms.append(perm)
        diff.append(np.abs(np.subtract(d_max_pca,d_max_ica[np.array(perm)])))
    diff=np.array(diff)
    best_ord=np.argmin(np.sum(diff,axis=1),axis=0)
    perms=np.array(perms)
    rot_seg_match=rot_seg[np.array(perms[best_ord])]
    return rot_seg_match
