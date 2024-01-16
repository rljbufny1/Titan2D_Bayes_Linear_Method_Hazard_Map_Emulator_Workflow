%**********************************************************************
% matlab script: view_phm_read_in_zgrid
%
% argument(s): elevation.grid
%
% input(s): elevation.grid
%
% output(s): xyz
%
% Based on Ramona's script with
% updates to reduce the size of the xyz matrix for large elevation grids
%**********************************************************************
function xyz=view_phm_read_in_zgrid(filename)

fid=fopen(filename,'r');
yada=fscanf(fid,'Nx=%g: X={%g,%g}\nNy=%g: Y={%g,%g',[3 2]);
fgets(fid);
fgets(fid); %'}\nElevation=\n' OR '}\nPileheight=\n'
%size(yada(1,1));
Nx=yada(1,1);
minx = yada(2,1);
maxx = yada(3,1);
%size(yada(1,2));
Ny=yada(1,2);
miny = yada(2,2);
maxy = yada(3,2);
xyz=zeros(Nx,Ny,3);
xyz(:,:,1)=((2*(0:(Nx-1))+0.5)/(2*Nx)*(maxx-minx)+minx)'*ones(1,Ny);

%xyz(1:10,1:10,1);
xyz(:,:,2)=ones(Nx,1)*(2*(0:(Ny-1))+0.5)/(2*Ny)*(maxy-miny)+miny;
%xyz(1:10,1:10,2);
xyz(:,:,3)=fscanf(fid,'%g',[Nx Ny]);
fclose(fid);

% rlj - Saving images is taking too long for large elevation grids.
% For example, when Nx=1024 and Ny=1024,
% Octave took over two hours to save P.png and SDP.png.
% Now completes in less than six minutes
size(xyz)
maxN = 512;
% https://www.mathworks.com/help/matlab/learn_matlab/array-indexing.html
step = max(1,max(floor(Nx/maxN), floor(Ny/maxN)))
xyz = xyz(1:step:end, 1:step:end, :);
size(xyz)
return

