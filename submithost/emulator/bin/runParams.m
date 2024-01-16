%**********************************************************************
% matlab script: runParams.m
%
% argument(s): datadir_, workingdir_, minvol, maxvol, BEDMIN,BEDMAX,
%     startutmecenin, startutmncenin, startradiusmaxin, ResamplePointsin,
%     westin, eastin, southin, northin)
%
% input(s): None
%
% output(s): runParams.mat
%**********************************************************************

% Create the run parameters MatLab/Octave .mat file,
% required for steps 1, 4, 8, and 10,
% using values read in from simulation.py.

function runParams(workingdir_,...
    minvolin, maxvolin, BEDMINin, BEDMAXin,...
    startutmecenin, startutmncenin, startradiusmaxin, ResamplePointsin, ...
    westin, eastin, southin, northin,...
    ewresolin, nsresolin)

    workingdir = strcat(workingdir_, '/');
    disp(workingdir);

    % Save parameters to runParams.mat
    
    minvol=minvolin;
    maxvol=maxvolin;
    BEDMIN=BEDMINin;
    BEDMAX=BEDMAXin;
    STARTUTMECEN=startutmecenin;
    STARTUTMNCEN=startutmncenin;
    STARTRADIUSMAX=startradiusmaxin;
    ResamplePoints=ResamplePointsin;
    
    if (westin==-1)
       disp('Missing or unexpected format for GRASS cellhd file');
       return;
    else
       west=westin;
    end
    if (eastin==-1)
       disp('Missing or unexpected format for GRASS cellhd file');
       return;
    else
       east=eastin;
    end
    if (southin==-1)
       disp('Missing or unexpected format for GRASS cellhd file');
       return;
    else
       south=southin;
    end
    if (northin==-1)
       disp('Missing or unexpected format for GRASS cellhd file');
       return;
    else
       north=northin;
    end
    if (ewresolin==-1)
       disp('Missing or unexpected format for GRASS cellhd file');
       return;
    else
       ewresol=ewresolin;
    end
    if (nsresolin==-1)
       disp('Missing or unexpected format for GRASS cellhd file');
       return;
    else
       nsresol=nsresolin;
    end
    
    % Get the grid dimensions from 
    % the pileheightrecord created with simulation_10_step.py

    # May have to install titan2d for the docker build
    #[Nx, Ny] = get_grid_dimensions(workingdir);
    Nx = 320
    Ny = 256
    
    disp(' ');
    disp('Creating runParams.mat...');
    
    filename = strcat(workingdir,'runParams.mat');
    %disp(filename)
    
    % Save variables
    
    save (filename, 'minvol','maxvol','BEDMIN','BEDMAX',...
       'STARTUTMECEN','STARTUTMNCEN','STARTRADIUSMAX','ResamplePoints',...
	  'west','east','south','north','ewresol','nsresol','Nx','Ny')

    % Check
    
    load (filename, 'minvol');
    load (filename, 'maxvol');
    load (filename, 'BEDMIN');
    load (filename, 'BEDMAX');
    load (filename, 'STARTUTMECEN');
    load (filename, 'STARTUTMNCEN');
    load (filename, 'STARTRADIUSMAX');
    load (filename, 'ResamplePoints');
    load (filename, 'west');
    load (filename, 'east');
    load (filename, 'south');
    load (filename, 'north');
    load (filename, 'ewresol');
    load (filename, 'nsresol');
    load (filename, 'Nx');
    load (filename, 'Ny');

    fprintf('\nrun parameters: \n\n');
    fprintf('minvol: %.8f\n', minvol);
    fprintf('maxvol: %.8f\n', maxvol);
    fprintf('BEDMIN: %.8f\n', BEDMIN);
    fprintf('BEDMAX: %.8f\n', BEDMAX);
    fprintf('STARTUTMECEN: %.8f\n', STARTUTMECEN);
    fprintf('STARTUTMNCEN: %.8f\n', STARTUTMNCEN);
    fprintf('STARTRADIUSMAX: %.8f\n', STARTRADIUSMAX);
    fprintf('ResamplePoints: %d\n', ResamplePoints);
    fprintf('west: %.8f\n', west);
    fprintf('east: %.8f\n', east);
    fprintf('south: %.8f\n', south);
    fprintf('north: %.8f\n', north);
    fprintf('e-w resol: %.8f\n', ewresol);
    fprintf('n-s resol: %.8f\n', nsresol);
    fprintf('Nx: %.8f\n', Nx);
    fprintf('Ny: %.8f\n', Ny);
   
return
