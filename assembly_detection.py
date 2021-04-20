import numpy as np
from sklearn.decomposition import PCA

#Function to detect significant neuronal assemblies
def assembly_detection(path,dmr,z_norm_mat):
    #Running PCA on the z_norm matrix
    N_clu=z_norm_mat.shape[0]
    N_bins=z_norm_mat.shape[1]
    N_eigen=N_clu
    pca=PCA()
    z_norm_proj=pca.fit(z_norm_mat.T)
    # Getting eigenvalues
    eig_vals=z_norm_proj.explained_variance_
    #Getting principal components
    eig_vecs=z_norm_proj.components_
    #Getting amount of variance explained
    expl_var=z_norm_proj.explained_variance_ratio_

    # Marcenko–Pastur eigenvalue threshold to identify significant assemblies
    q=N_bins/N_clu
    sigma=1
    lambda_max=(sigma**2)*((1+np.sqrt(1./q)))**2
    lambda_min=(sigma**2)*((1-np.sqrt(1./q)))**2

    # Extracting significant eigenvectors
    sig_eig_vec=[]
    bel_lam_min_vec=[]
    for eig in range(N_eigen):
        if eig_vals[eig]>lambda_max:
            sig_eig_vec.append(eig_vecs[eig])

        elif eig_vals[eig]<lambda_min:
            bel_lam_min_vec.append(eig_vecs[eig])

    sig_eig_vec=np.array(sig_eig_vec)
    bel_lam_min_vec=np.array(bel_lam_min_vec)
    print('Number of significant assemblies from '+str(path)+', dmr '+str(dmr)+': '+str(sig_eig_vec.shape[0]))
    #print('Expected number of neurons per assembly: '+str(bel_lam_min_vec.shape[0]))


    return  sig_eig_vec,bel_lam_min_vec,expl_var
