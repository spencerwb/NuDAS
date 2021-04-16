function o = testRetString(i)
    m = load('spike_matrix_0.001.mat');
    m.spt_mat(1, 1) = 53;
    m.spt_mat(:,:) = i;
    
    save('./output.mat','m')
    
    disp('hello helloooo')
    
    o = i + 1

end