%**********************************************************************
% matlab script: gen_random_macro_emulator_resample_inputs.m
%
% argument(s): datadir_
%
% input(s): runParams.mat
%
% output(s): macro_resamples.tmp
%**********************************************************************

% Resamples should be drawn from the DISTRIBUTION not just the range
% of the sample inputs
function gen_random_macro_emulator_resample_inputs(datadir_)

    datadir = strcat(datadir_, '/');
    
    ifplot=0;
    
    % Read in run parameters
    
    filename = strcat(datadir, 'runParams.mat');
    filename
    
    if exist(filename, 'file')
        
       load (filename, 'minvol');
       load (filename, 'maxvol');
       load (filename, 'BEDMIN');
       load (filename, 'BEDMAX');
       load (filename, 'STARTUTMECEN');
       load (filename, 'STARTUTMNCEN');
       load (filename, 'STARTRADIUSMAX');
       load (filename, 'ResamplePoints');

    else
       disp('runParams.mat not found');
       return;
    end

    minlog10vol = log10(minvol);
    maxlog10vol = log10(maxvol);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %these 2 parameters are from the SAMSI technometrics paper for Montserrat.  
    % TODO: Provide a mechanism for users to enter this historial information
    lambda=12425; %events per year
    alpha=0.65; %pareto exponent, unitless    
    Years=10;
    
    %probability of log10volume=
    %Years*lambda*alpha*log(10)*(vol.^-alpha).*exp(-Years*lambda*vol.^-alpha);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %direction historical frequency
    histangle=[...
         20 573;...
         78 151;...
         90  17;...
         98 230;...
        125  37;...
        143  87;...
        180  89;...
        230   1;...
        270  80];
    NHist=sum(histangle(:,2));
    SumHistAng=cumsum(histangle(:,2));
    IHistAng=repmat(length(histangle),NHist,1);
    for ii=length(histangle)-1:-1:1
        IHistAng(1:SumHistAng(ii))=ii;
    end
    rand('twister',5489);
    IHistAng=IHistAng(randperm(NHist));
      
    NxmacroWant=ResamplePoints;
    Nxmacro=2^round(log2(ResamplePoints));
    if(Nxmacro~=NxmacroWant)
        warning('Nxmacro rounded from %g to %g',NxmacroWant,Nxmacro);
    end
    
    %rand('seed',0);

    filename = strcat(datadir, 'macro_resamples.tmp');
    fid=fopen(filename,'w');
    fprintf(fid,'additional file format lines=%g\n',3);

    fprintf(fid,'%%Ndiminmacro=4: #of macro-emulator inputs (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [1] integer\n');
    fprintf(fid,'%%Nxmacro: the number of macro emulator input points to evaluate: [1] integer\n');
    fprintf(fid,'%%{{x=(log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [Nxmacro Ndiminmacro] doubles},{w: relative weight for hazmap assembly, sum(w)~=1 is ok: [1] double}}\n');

    Ndiminmacro=4;
    
    rand('twister',5489);
    % Octave does not provide a lhsdesign function
    %r=lhsdesign(Nxmacro,Ndiminmacro);
    r=BinOptLHSRand(Ndiminmacro,Nxmacro);
    
    vol=minvol+(maxvol-minvol)*r(:,1);
    log10vol = log10(vol);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %probability of log10(volume)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    %%{
    pdraw=1/(maxlog10vol-minlog10vol); 
    pfrechet=Years*lambda*alpha*log(10)*(vol.^-alpha).*exp(-Years*lambda*vol.^-alpha);  

    w=pfrechet./pdraw; %non normalized likelihood ratio for importance sampling
    sumwdivNxmacro=sum(w)/Nxmacro
    w=w/mean(w);
    %}
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Direction
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%save DEBUGME;
    %Direction=histangle(IHistAng(ceil(NHist*r(:,2))),1);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Friction Angles
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %BEDFRICTANG=BEDMIN+(BEDMAX-BEDMIN)*r(:,3);
    BEDFRICTANG=BEDMIN+(BEDMAX-BEDMIN)*r(:,2);
    %INTFRICTANG=BEDFRICTANG+17+7*r(:,4);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %STARTUTMECEN=197232;
    %STARTUTMECEN = minUTME + (maxUTME - minUTME) / 2.0;
    %STARTUTMNCEN=120224;
    %STARTUTMNCEN = minUTMN + (maxUTMN - minUTMN) / 2.0;
    %STARTRADIUSMAX=750; %350*SafetyFactor;
    STARTRADIUS=STARTRADIUSMAX*sqrt(r(:,3));
    UTME=STARTUTMECEN+STARTRADIUS.*cos(2*pi*r(:,4));
    UTMN=STARTUTMNCEN+STARTRADIUS.*sin(2*pi*r(:,4));
    
    %plot(UTME, UTMN, 'bx'); axis equal;
    
    fprintf(fid,'%d\n%d\n',Ndiminmacro,Nxmacro);
    %fprintf(fid,'%.10g %.10g %.10g %.10g %.10g\n',[log10vol Direction BEDFRICTANG INTFRICTANG w]');
    % This needs to be consistent with uncertain_input_list.txt
    fprintf(fid,'%.10g %.10g %.10g %.10g\n',[log10vol UTME UTMN BEDFRICTANG w]');
    
    fclose(fid);
    
     if(ifplot)
        fig=figure;
        pos=get(fig,'position');
        pos(2)=pos(2)-0.5*pos(4);
        pos(4)=pos(4)*1.5;
        set(fig,'position',pos,'paperunits','inches','paperposition',[.75 1 7 9]);
        
        %subplot(3,2,1);
        %plot(log10vol,Direction,'bx'); axis square; %axis([minlog10vol maxlog10vol STARTUTMECEN+STARTRADIUSMAX*[-1 1]]);
        %xlabel('log10(vol)');
        %ylabel('Direction [deg]');

        subplot(3,2,2);
        plot(log10vol,BEDFRICTANG,'bx'); axis image; %square; axis([minlog10vol maxlog10vol BEDMIN BEDMAX]);
        xlabel('log10(vol)');
        ylabel('\phi_{bed} [deg]');

        %subplot(3,2,3);
        %plot(log10vol,INTFRICTANG,'bx'); axis image; %square; axis([minlog10vol maxlog10vol BEDMIN BEDMAX]);
        %xlabel('log10(vol)');
        %ylabel('\phi_{int} [deg]'); 

        %subplot(3,2,4);
        %plot(Direction,BEDFRICTANG,'bx'); axis square; %axis([STARTUTMECEN+STARTRADIUSMAX*[-1 1] BEDMIN BEDMAX]);
        %xlabel('Direction [deg]');
        %ylabel('\phi_{bed} [deg]');        
        
        %subplot(3,2,5);
        %plot(Direction,INTFRICTANG,'bx'); axis square; %axis([STARTUTMECEN+STARTRADIUSMAX*[-1 1] BEDMIN BEDMAX]);
        %xlabel('Direction');
        %ylabel('\phi_{int} [deg]');
                
        %subplot(3,2,6);
        %plot(BEDFRICTANG,INTFRICTANG,'bx'); axis image; %square; axis([STARTUTMNCEN+STARTRADIUSMAX*[-1 1] BEDMIN BEDMAX]);
        %xlabel('\phi_{bed} [deg]');
        %ylabel('\phi_{int} [deg]');        
    end
        
return;
