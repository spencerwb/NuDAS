function mat=run_granger()
    mat=load('spike_matrix_0.001.mat');
    spt_mat=mat.spt_mat;
    tot_duration=60000;
    trial_duration=3000;
    spt_mat_trunc=spt_mat(:,1:tot_duration);
    X=reshape(spt_mat_trunc,size(spt_mat_trunc,1),trial_duration,tot_duration/trial_duration);
    demo_real(X);

end
