%**********************************************************************
% matlab script: Gen_Titan_Input_Samples.m
%
% argument(s): datadir_,Nymacro(the number of samples)
%
% input(s): runParams.mat
%
% output(s): uncertain_input_list.txt, uncertain_input_list_h.txt
%**********************************************************************

function Gen_Titan_Input_Samples(datadir_, Nymacro)

    datadir = strcat(datadir_, '/');
    
    if(ischar(Nymacro))
      Nymacro=str2num(Nymacro);
    end
    %disp(Nymacro);

    Ndiminmacro=4;
    
    ifplot=0;

    % Read in run parameters
    
    filename = strcat(datadir, 'runParams.mat');
    %filename
    
    if exist(filename, 'file')
        
       load (filename, 'minvol');
       load (filename, 'maxvol');
       load (filename, 'BEDMIN');
       load (filename, 'BEDMAX');
       load (filename, 'STARTUTMECEN');
       load (filename, 'STARTUTMNCEN');
       load (filename, 'STARTRADIUSMAX');

    else
       disp('runParams.mat not found');
       return;
    end
    
    rand('twister',5489)
    %rand('seed',0);
    % Octave does not provide a lhsdesign function
    %r=lhsdesign(Nymacro,Ndiminmacro);
    r=BinOptLHSRand(Ndiminmacro,Nymacro);
    % For testing only:
    %fprintf('size(r): %s\n', mat2str(size(r))); %[32 4]
    %fprintf('r: [%s]\n', mat2str(r));
    %r = flipud (r);
    %fprintf('r: [%s]\n', mat2str(r));

    vol=minvol+(maxvol-minvol)*r(:,1);
    h=(vol/pi).^(1/3);
    radius=h;
    
    %log10vol=(maxlog10vol-minlog10vol)*5*r(:,1)+minlog10vol;
    %radius=((10.^log10vol).*(2/pi)).^(1/3);
    
    BEDFRICTANG=BEDMIN+(BEDMAX-BEDMIN)*r(:,2);
    %UTME=minUTME+(maxUTME-minUTME)*r(:,3);
    %UTMN=minUTMN+(maxUTMN-minUTMN)*r(:,4);
        
    STARTRADIUS=STARTRADIUSMAX*sqrt(r(:,3));
    UTME=STARTUTMECEN+STARTRADIUS.*cos(2*pi*r(:,4));
    UTMN=STARTUTMNCEN+STARTRADIUS.*sin(2*pi*r(:,4));
    
    %UTME=minUTME+(maxUTME-minUTME).*cos(2*pi*r(:,3));
    %UTMN=minUTMN+(maxUTMN-minUTMN).*sin(2*pi*r(:,3));
    %INTFRICTANG=INTMIN+(INTMAX-INTMIN)*r(:,4);
    %maxbedfrict=max(BEDFRICTANG)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %plot(UTME,UTMN,'or')
    %plot(UTME,UTMN,'bx'); axis equal;
    
    filename = strcat(datadir, 'uncertain_input_list.txt');
    fid=fopen(filename,'w');
    fprintf(fid,'additional file format lines=3\n');
    fprintf(fid,'%%Ndiminmacro=4: of macro-emulator input dimensions (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [1] integer\n');
    fprintf(fid,'%%Nymacro: number of simulations/mini-emulators: [1] integer\n');
    fprintf(fid,'%%log10(volume [m^3]), UTME, UTMN, BedFrictAng [deg], ): [Nymacro Ndiminmacro] array of doubles\n');
    fprintf(fid,'%g\n',Ndiminmacro,Nymacro);
    fprintf(fid,'%.10g %.10g %.10g %.10g\n',[log10(vol) UTME UTMN BEDFRICTANG]');
    fclose(fid);
    
    filename = strcat(datadir, 'uncertain_input_list_h.txt');
    fid=fopen(filename,'w');
    fprintf(fid,'additional file format lines=3\n');
    fprintf(fid,'%%Ndiminmacro=4: of macro-emulator input dimensions (log10(volume [m^3]),UTMN, UTME, bedfric): [1] integer\n');
    fprintf(fid,'%%Nymacro: number of simulations/mini-emulators: [1] integer\n');
    fprintf(fid,'%%y=(h radius UTME UTMN bedfric): [Nymacro Ndiminmacro] array of doubles\n');
    fprintf(fid,'%g\n',Ndiminmacro,Nymacro);
    fprintf(fid,'%.10g %.10g %.10g %.10g %.10g\n',[h radius UTME UTMN BEDFRICTANG]');
    fclose(fid);
return
    
   
    
    
    
