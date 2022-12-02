clear 
close all
clc
%% ----------------------- (a) --------------------------------------------

% Setting parameters
r0 = 50;
t = 0:0.01:500;
tau = 0:0.01:0.3;
stim = zeros(size(t));

% Constructing Stimulus
for i=1:size(t, 2)
    stim(1, i) = normrnd(0, sqrt(2));
end

% Constructing Kernel D(tau)
for i=1:size(tau, 2)
    D(1, i) = -cos(2*pi*(tau(1, i)*1000 - 20)/140) * exp(-tau(1, i) * 1000/60);
end

% Calculating r_est(t) from equation (2.1)
D = flip(D);
for i=1:size(t, 2)
    if i < size(tau, 2)
        d = D(1, 1:i);
        s = stim(1, 1:i);
        r_est(1, i) = r0 + sum(d.*s);
    end
    if i >= size(tau, 2)
        s = stim(1, i-size(tau, 2)+1:i);
        r_est(1, i) = r0 + sum(D.*s);
    end
end

[est,K,ind]=c3p10(stim(1, :),r_est(1, :),1024);

%% ==========================================
%% ******  This Function doesn't work  ******
%%     SPECTRUM finction has been deprecated
%%     Which was used in 'c3p10'
%% ==========================================













