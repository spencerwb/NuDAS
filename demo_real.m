function demo_real(X)

[CHN SMP TRL] = size(X);
disp(size(X))
disp(TRL)
% To fit GLM models with different history orders
for neuron = 1:CHN
    for ht = 3:3:60                             % history, W=3ms
        [bhat{ht,neuron}] = glmtrial(X,neuron,ht,3);
    end
end
ht_min_criterion=zeros(1,8)
% To select a model order, calculate AIC
hts=3:3:60
for neuron = 1:CHN
    for ht = 3:3:60
        LLK(ht,neuron) = log_likelihood_trial(bhat{ht,neuron},X,ht,neuron);
        aic(ht,neuron) = -2*LLK(ht,neuron) + 2*(CHN*ht/3 + 1);
    end
    [min_val,ind]=min(aic(hts,neuron));
    ht_min_criterion(neuron)=ind;
end

% Identify Granger causality
CausalTest(X,bhat,aic,LLK,ht_min_criterion)
end
