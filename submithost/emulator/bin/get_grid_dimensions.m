%**********************************************************************
% matlab script: get_grid_dimensions.m
%
% argument(s): datadir_
%
% input(s): pileheightrecord.-00001
%
% output(s): grid dimensions Nx and Ny
%**********************************************************************

function [Nx, Ny]=get_grid_dimensions(datadir_)

    datadir = strcat(datadir_, '/');

    % Get the grid dimensions Nx (Neast) and Ny (Nnorth) for the 
    % initial hazard map
    
    filename=strcat(datadir, 'pileheightrecord.-00001');
    fid=fopen(filename,'r');
    if(fid==-1)
        fprintf('error opening the pile height record %s\n',filename);
        return;
    end
    fclose(fid);
    XYH=read_in_zgrid(filename);
    
    X=XYH(:,:,1);
    Y=XYH(:,:,2);
    H=XYH(:,:,3);
    clear XYZ s w;
    [Nx,Ny]=size(X);

return
