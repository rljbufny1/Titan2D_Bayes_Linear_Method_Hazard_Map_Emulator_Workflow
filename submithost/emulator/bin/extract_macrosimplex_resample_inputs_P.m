%**********************************************************************
% matlab script: extract_macrosimplex_resample_inputs_P.m
%
% argument(s): datadir_,macrosimplexnumber,Ndimimmacrox,Nxmap,xmap,maxmacrosperifle 
%
% input(s): macro_resample_assemble.inputs
%
% output(s): eval_resamples_for_simplex_<simplex id string>
%**********************************************************************

function extract_macrosimplex_resample_inputs_P ...
    (datadir_,macrosimplexnumber,uniquesimplexkey,NdiminmacroX,Nxmap,xmap,maxmacrosperfile)

    datadir = strcat(datadir_, '/');
    
    if(ischar(macrosimplexnumber))
        macrosimplexnumber=str2double(macrosimplexnumber);
    end
    if(ischar(maxmacrosperfile))
        maxmacrosperfile=str2double(maxmacrosperfile);
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %read in input file #1
    %This should really be done in the calling routine
    
    filename = strcat(datadir, 'macro_resample_assemble.inputs');
    fid=fopen(filename,'r');
    
    Nskip=sscanf(fgets(fid),'additional file format lines=%g',1);
    for i=1:Nskip
        fgets(fid);
    end
    %fprintf(fid,'%%Ndiminmacro=4: of macro-emulator input dimensions (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [1] integer\n');
    %fprintf(fid,'%%Nxmacroinside: the number of macro emulator (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]) input points to evaluate: [1] integer\n');    
    %fprintf(fid,'%%{{(log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [Ndiminmacro] doubles},{isimp: index of  macro-emulator simplex: [1] integer},{simulation/mini-emulator indices/ids: [Ndiminmacro+1] integers},{barycentric coordinates: [Ndiminmacro+1] doubles},{w: relative weight for hazmap assembly, sum(w)~=1 is ok: [1] double}}\n');
    %fprintf(fid,'%%Nxmacrooutside: the number of randomly generated input points that can''t evaluate because they lie outside the convex hull of simulations\n');
    %fprintf(fid,'%%{{(log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [Ndiminmacro] doubles},{w: relative weight for hazmap assembly: [1] double}}\n');
    
    Ndiminmacro  =sscanf(fgets(fid),'%g',1);
    Nxmacroinside=sscanf(fgets(fid),'%g',1);
    yada=sprintf('%s%%g\n',repmat('%g ',1,Ndiminmacro+1+(Ndiminmacro+1)*2));
    evalthesemacro=fscanf(fid,yada,[(Ndiminmacro+1)*3+1 Nxmacroinside])';
    ievalthesemacro=find(evalthesemacro(:,Ndiminmacro+1)==macrosimplexnumber);
    Nmacroseachx=numel(ievalthesemacro);
    Nuniquemacroeachx=Nmacroseachx;
    evalthesemacro=evalthesemacro(ievalthesemacro,:);
    nodesofsimplex=unique(evalthesemacro(:,Ndiminmacro+1+(1:Ndiminmacro+1)),'rows');
    if(size(nodesofsimplex,1)>1)
        save DEBUG_EXTRACT_MACROSIMPLEX_RESAMPLE1;
        disp(sprintf('Error: there are %g SETS of nodes for simplex %g!!!! Workspace saved to DEBUG_EXTRACT_MACROSIMPLEX_RESAMPLE1.mat\n',size(nodesofsimplex,1),macrosimplexnumber));
        bob; %cause the code to crash
    elseif(Nmacroseachx==0)
        nodesofsimplex=repmat(-1,1,Ndiminmacro+1);        
    end
    evalthesemacro=evalthesemacro(:,1:Ndiminmacro);
    fclose(fid);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %{
    %read in input file #2
    fid=fopen(hazmapfilename,'r');
    Nskip=sscanf(fgets(fid),'additional file format lines=%g',1);
    for i=1:Nskip
        fgets(fid);
    end
%     fprintf(fid,'%%This file contains data for a probability of hazard map generated by resampling a piecewise linear ensemble emulator constructed from titan simulations\n');
%     fprintf(fid,'%%crith [m]: the critical flow depth in meters, a .phm file contains the data needed to plot a map of P(h(east,north)>crith): [1] double\n');
%     fprintf(fid,'%%Ndiminmacro=4: number of uncertain dimensions (see what they are below) for each resample input: [1] integer\n');
%     fprintf(fid,'%%W: total so far weight of all resamples (macro emulator inputs) used to make this file:  [1] double\n');
%     fprintf(fid,'%%Nxmap: the number of (east,north) points on the map directly represented by this file: [1] integer\n');
%     fprintf(fid,'%%[Nxmap] lines containing {{x=(east,north):[2] doubles},{{WI WI^2}: these are the sum of all w*indicator_function and w*indicator_function^2, you compute the probability of exceeding the critical height as P(h(east,north)>crith)=WI/W: [2] doubles}}\n');
%     fprintf(fid,'%%Nresamp: number of resample inputs used so far to produce this .phm file: [1] integer\n');
%     fprintf(fid,'%%[Nresamp] lines containing the {{resample macro-inputs: (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): [Ndiminmacro] doubles},{w: weight of this resample macro-input: [1] double}}\n');
    
    
    crith=sscanf(fgets(fid),'%g',1); %don't need this
    NdiminmacroX=sscanf(fgets(fid),'%g',1);
    W=sscanf(fgets(fid),'%g',1); %don't need this
    Nxmap=sscanf(fgets(fid),'%g',1);

    if(Ndiminmacro~=NdiminmacroX)
        save DEBUG_EXTRACT_MACROSIMP_RESAMPLE2;
        disp(sprintf('ERROR: Ndiminmacro from "macro_resample_assemble.inputs" ~= Nidminmacro from "%s"!!!! Workspace saved to DEBUG_EXTRACT_MACROSIMP_RESAMPLE2.\n',hazmapfilename));
        bob; %cause the code to crash
    end

    xmap=fscanf(fid,'%g',[4 Nxmap])';
    xmap=xmap(:,1:2);    
    fclose(fid);
    %}
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %now need to merge evalthesemacro and xmap

    fileformatoption=1; %can also choose "2," which is more general but also a LOT larger
    %rand('twister',sum(100*clock)); %initialize random number generator to a different number each time this function is called 
    % rlj for testing only
    %rand('twister',5489); %initialize random number generator to a different number each time this function is called 
    
    Ndiminspatial=2; %east and north
    Nxspatial=Nxmap;
    
    Nfiles=ceil(Nmacroseachx/maxmacrosperfile);
    %uniquesimplexkey=zeros(1,Nfiles);
    NmacrosSoFar=0;
    
    for ifile=1:Nfiles
        nmacroseachx=min(maxmacrosperfile,Nmacroseachx-NmacrosSoFar);
        ithesemacros=NmacrosSoFar+(1:nmacroseachx);
        
        %macro simplex number is an integer, r=rand() produces a random
        %number uniformly distributed such that 0<r<1
        %uniquesimplexkey(ifile)=macrosimplexnumber+rand(1);
        uniquesimplexkeystring=sprintf('%.8f',uniquesimplexkey(ifile));     
    
        filename = strcat(datadir, sprintf('eval_resamples_for_simplex_%s',uniquesimplexkeystring));
        fid=fopen(filename,'w');
    
        Nskip=13;
        fprintf(fid,'additional file format lines=%g\n',Nskip);
    
        fprintf(fid,'%%Unique Key: the number before the decimal is the simplex id. The number AFTER THE DECIMAL is randomly generated after seeding by clock and also occurs in mini-emulator evaluation output filenames allowing you to match them: [1] double\n');
        fprintf(fid,'%%Ndiminmacro=4: #of uncertain dimensions, (log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]) for each resample input: [1] integer\n');
        fprintf(fid,'%%{{(simplex id): a sanity check: [1] integer},{id''s of simulation/mini-emulator in the simplex: [Ndiminmacro+1] integers}}\n');
        fprintf(fid,'%%Ndiminspatial=2: #of spatial dimensions (east,north): [1] integer\n');
        fprintf(fid,'%%Nmacroseachx: #of macro input points associated with each spatial point, done to reduce file size but remain general: [1] integer\n');
        fprintf(fid,'%%Nxspatial: #of LISTED spatial coordinates: [1] integer\n');
        fprintf(fid,'%%file format option indicator: [1] integer\n');
        fprintf(fid,'%%one of the following two options\n');
        fprintf(fid,'%%option 1: for when all spatial points need to be evaluated at the same set(s) of macro coordinates\n');
        fprintf(fid,'%%     one line containing: [Nmacroseachx] sets of {(log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): macro input coordinates: [Ndiminmacro] doubles}\n');
        fprintf(fid,'%%     [Nxspatial] lines containing {(east,north): [2] doubles}\n');
        fprintf(fid,'%%option 2: for when each spatial point can be paired with different macro input(s), in this case there can also be duplicates of listed (east,north) coordinates that have different macro coordinates\n');
        fprintf(fid,'%%     [Nxspatial] lines containing {{(east,north): [2] doubles},{[Nmacroseachx] sets of {(log10(volume [m^3]),Direction [deg CC from east],BedFrictAng [deg],IntFrictAng [deg]): macro input coordinates: [Ndiminmacro] doubles}}}\n');
    
        fprintf(fid,'%s\n',uniquesimplexkeystring);
        fprintf(fid,'%g\n',Ndiminmacro);
        fprintf(fid,sprintf('(%g)%s\n',macrosimplexnumber,repmat(' %g',1,Ndiminmacro+1)),nodesofsimplex);
        fprintf(fid,'%g\n',Ndiminspatial,nmacroseachx,Nxspatial,fileformatoption);
        switch(fileformatoption)
            case 1,
                yada=sprintf('%%.10g%s\n',repmat(' %.10g',1,nmacroseachx*Ndiminmacro-1));
                fprintf(fid,yada,evalthesemacro(ithesemacros,:)');
                fprintf(fid,'%.2f %.2f\n',xmap');
            case 2,
                yada=sprintf('%%.2f %%.2f%s\n',repmat(' %.10g',1,nmacroseachx*Ndiminmacro));
                fprintf(fid,yada,[xmap repmat(reshape(evalthesemacro',1,nmacroseachx*Ndiminmacro),Nxmap,1)]');
            otherwise,
                save DEBUG_EXTRACT_MACROSIMP_RESAMPLE3;
                disp(sprintf('ERROR: unknown output file format option!!!! Workspace saved to DEBUG_EXTRACT_MACROSIMP_RESAMPLE3.\n'));
                bob; %cause the code to crash
        end
        fclose(fid);
        NmacrosSoFar=NmacrosSoFar+nmacroseachx;
    end
    uniquesimplexkey=sprintf(sprintf('%%.8f%s',repmat(' %.8f',1,Nfiles-1)),uniquesimplexkey);
    %uniquesimplexkey=num2str(uniquesimplexkey,'%.8f');
    
return
