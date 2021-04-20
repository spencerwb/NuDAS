import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA
# Computes the participation of each neuron to each significant assembly
def neuronal_participation(z_norm_mat,sig_eig_vec):
    #PCA
    pca=PCA(n_components=sig_eig_vec.shape[0])
    z_norm_proj=pca.fit_transform(z_norm_mat.T)

    #ICA on the subspace spanned by the siginificant principal components
    ica=FastICA(n_components=sig_eig_vec.shape[0])
    z_norm_trans=ica.fit(z_norm_proj)

    #Rotates the principal components
    rot_seg=ica.transform(sig_eig_vec.T).T
    #rot_seg=np.matmul(z_norm_trans.components_,sig_eig_vec)
    for r in range(rot_seg.shape[0]):
        rot_seg[r]=rot_seg[r]/np.linalg.norm(rot_seg[r])
        am=np.argmax(np.abs(rot_seg[r]))
        if rot_seg[r,am]<0:
            rot_seg[r]=-rot_seg[r]
    return rot_seg
