%**********************************************************************
% matlab script: script11_12_13_stage.m
%
% argument(s): datadir_
%
% input(s): macro_emulator.pwem, macro_resample_assemble.inputs, 
%   AZ_vol_dir_bed_int.phm
%
% output(s): step11_12_13_staged_input.txt
%**********************************************************************

function script11_12_13_stage(datadir_)

    % Modified from script11_14.m
    % for running extract_macrosimplex_resample_inputs,
    % evaluate_mini_emulator_mean and assemble_minis_to_macro_to_phm

    datadir = strcat(datadir_, '/');
    
    filename = strcat(datadir, 'macro_emulator.pwem');
    fid=fopen(filename,'r');

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

    filename = strcat(datadir, 'step11_12_13_staged_input.txt');
    fprintf('\nCreating staged input file %s...\n', filename);

    fid=fopen(filename,'w');

    checkPercent = 10;
    if (dim > checkPercent)
        done = 0;
        nextDoneIncrement = dim/checkPercent;
        nextDoneCheck = done + nextDoneIncrement;
        nextDonePercent = 0;
    end

    for i=1:dim

        if (dim > checkPercent)
            done = done + 1;
            if (done > nextDoneCheck)
               nextDoneCheck = done + nextDoneIncrement;
               nextDonePercent = nextDonePercent + checkPercent;        
               fprintf ("%d percent complete...\n", nextDonePercent)
            end
        end

        %i
        % Setting 100 is making Nfiles = 1
        a=get_macrosimplex_resample_inputs_P(datadir_,i,NdiminmacroX,Nxmap,xmap,100);
        anum=sscanf(a,'%g',[1,inf]);
        if (anum)
           fprintf(fid,'%s\n', a);
        else
           fprintf(fid, '0\n');
        end
    end
    
    fclose (fid);
    fprintf('Staged input file successfully created\n\n');
end
