function CausalTest(X,bhat,aic,LLK,ht_min_criterion)


[CHN SMP TRL] = size(X);

% Selected spiking history orders by AIC
ht = ht_min_criterion

% Re-optimizing a model after excluding a trigger neuron's effect and then
% Estimating causality matrices based on the likelihood ratio

for target = 1:CHN
    LLK0(target) = LLK(3*ht(target),target);
    for trigger = 1:CHN
        % MLE after excluding trigger neuron
        [bhatc{target,trigger},devnewc{target,trigger}] = glmtrialcausal(X,target,trigger,3*ht(target),3);

        % Log likelihood obtained using a new GLM parameter and data, which
        % exclude trigger
        LLKC(target,trigger) = log_likelihood_trialcausal(bhatc{target,trigger},X,trigger,3*ht(target),target);

        % Log likelihood ratio
        LLKR(target,trigger) = LLKC(target,trigger) - LLK0(target);

        % Sign (excitation and inhibition) of interaction from trigger to target
        % Averaged influence of the spiking history of trigger on target
        SGN(target,trigger) = sign(sum(bhat{3*ht(target),target}(ht(target)*(trigger-1)+2:ht(target)*trigger+1)));
    end
end

% Granger causality matrix, Phi
Phi = -SGN.*LLKR;

% ==== Significance Testing ====
% Causal connectivity matrix, Psi, w/o FDR
D = -2*LLKR;                                     % Deviance difference
alpha = 0.05;
for ichannel = 1:CHN
    temp1(ichannel,:) = D(ichannel,:) > chi2inv(1-alpha,ht(ichannel)/2);
end
Psi1 = SGN.*temp1;

% Causal connectivity matrix, Psi, w/ FDR
fdrv = 0.05;
temp2 = FDR(D,fdrv,ht);
Psi2 = SGN.*temp2;


save('./causal_map.mat','Psi2')
clear all;
