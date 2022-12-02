function [est,K,ind]=c3p10(stim,spk,nfft)%[est,K,sstim]=wf(stim,spk,nfft)%Finds the optimal decoding filter K to predict stim from spk using %matlab function spectrum with nfft frequencies%est    is the resulting stimulus estimate%K      is the filter%ind    is the indices such that est approximmates stim(ind).spk=spk-mean(spk);        % remove the mean of the spikesmstim=mean(stim);         stim=stim-mstim;          % remove the mean of the stimulusP=spectrum(spk,stim,nfft); % work out the various self- and                           % cross-spectral termsTxy=P(:,4);                % the complex transfer function from X to Y --                           % ie the FFT of the decoding filterT=[Txy ; conj(Txy((end-1):-1:2))]; % want the real-valued versionK=fftshift(real(ifft(T)));% shift to make it centeredest=fftfilt(K,spk);       % use the fast filter algorithmest=est(nfft+1:end)+mstim; % get rid of the transientind=(nfft/2+1):(length(stim)-nfft/2); % the indices of stim that                                      % match those of est                                       					                                         