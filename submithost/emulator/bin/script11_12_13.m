%**********************************************************************
% matlab script: script11_12_13.m
%
% argument(s): datadir_, start simplex number, stop simplex number
%
% input(s): step11_12_13_staged_input.txt, macro_emulator.pwem, 
%   macro_resample_assemble.inputs, AZ_vol_dir_bed_int.phm, 
%   mini_emulator.<sample number - formatted as %06d>
%   (needs all the mini_emulator files)
%
% output(s): phm_from_eval* files for 
%   start simplex number through stop simplex number
%**********************************************************************

function script11_12_13(datadir_,start_simplex_number,stop_simplex_number)

    % Modified from script11_14.m
    % for running extract_macrosimplex_resample_inputs,
    % evaluate_mini_emulator_mean and assemble_minis_to_macro_to_phm

    datadir = strcat(datadir_, '/');
    
    filename = strcat(datadir, 'macro_emulator.pwem');
    fid=fopen(filename,'r');
    
    fprintf ('script11_13 start_simplex_number: %d\n', start_simplex_number);
    fprintf ('script11_13 stop_simplex_number: %d\n', stop_simplex_number);

    Nskip=sscanf(fgets(fid),'additional file format lines=%g',1);
    for i=1:Nskip
        fgets(fid);
    end
    Ndiminmacro  =sscanf(fgets(fid),'%g',1);
    Nxmacroinside=sscanf(fgets(fid),'%g',1);
    for i=1:Nxmacroinside
        fgets(fid);
    end
    %dim=fscanf(fid, '%g',1)
    %y1=fscanf(fid, '%g', [5 dim])';
    %y=y1(:,2:6);
    dim=sscanf(fgets(fid),'%g',1) %number of simplices (triangles)
    yada=sprintf('(%%g)%s\n',repmat(' %g',1,Ndiminmacro+1));
    tess=fscanf(fid,yada,[Ndiminmacro+2 dim])';
    y=tess(:,2:6);
    sizey = size(y);
    fclose(fid);

    hazmapfilename = strcat(datadir, 'AZ_vol_dir_bed_int.phm');

    disp(dim);

    %maxkzero = 0;
    %maxknonzero = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%read in input file hazmapfilename
%%{
fid=fopen(hazmapfilename,'r');
Nskip=sscanf(fgets(fid),'additional file format lines=%g',1);
for i=1:Nskip
    fgets(fid);
end
crith=sscanf(fgets(fid),'%g',1); %don't need this
NdiminmacroX=sscanf(fgets(fid),'%g',1);
W=sscanf(fgets(fid),'%g',1); %don't need this
Nxmap=sscanf(fgets(fid),'%g',1);
    
xmap=fscanf(fid,'%g',[4 Nxmap])';
xmap=xmap(:,1:2);    
fclose(fid);
%}

filename = strcat(datadir, 'step11_12_13_staged_input.txt');
fid=fopen(filename,'r');
%status = feof(fid)
%position=ftell(fid)

anum_array = zeros (dim, 1);

% This will have to be done beforehand
for i=1:dim
   str = fgetl(fid);
   anum_array(i) = sscanf(str, '%g', 1);
end

fclose(fid);

for i=start_simplex_number:stop_simplex_number
    
    if (anum_array(i))
    printf ('anum_array(%d): %.8f\n', i, anum_array(i));
    %a=extract_macrosimplex_resample_inputs_P(i,hazmapfilename,100);
    extract_macrosimplex_resample_inputs_P(datadir_,i,anum_array(i),NdiminmacroX,Nxmap,xmap,100);
    %anum=sscanf(a,'%g',[1,inf]);
    %maxk = numel(anum)
    %maxk
    maxk = 1
    %if (maxk == 0)
      %maxkzero = maxkzero + 1;
    %else
      %maxknonzero = maxknonzero + 1;
    %end
    for k=1:maxk
        macrosimplex_resample_filename = ...
        strcat(datadir, sprintf('eval_resamples_for_simplex_%.8f',anum_array(i)));
        for j=1:sizey(2)
            j
            y(i,j)
            evaluate_mini_emulator_mean(datadir_,y(i,j),macrosimplex_resample_filename);
        end
        
        aminievalfilename = ... 
           strcat(datadir, sprintf('mini_emulator_eval_%.8f.1.%06d',anum_array(i),y(i,j)));       
       
        % assemble_minis_to_macro_to_phm and merge_probability_of_hazard_maps
        % abort by invoking an unknown command 'bob' on errors
        %newhazmapfilename = assemble_minis_to_macro_to_phm(aminievalfilename,hazmapfilename);
        assemble_minis_to_macro_to_phm_P(datadir_,aminievalfilename,crith,NdiminmacroX,Nxmap,xmap);
        %merge_probability_of_hazard_maps(hazmapfilename,newhazmapfilename);
    end
    end
end
end

%maxkzero

%maxknonzero
