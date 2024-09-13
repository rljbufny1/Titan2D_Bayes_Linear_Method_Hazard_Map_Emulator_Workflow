import numpy as np
import re

def read_in_zgrid(proj_in, geodetic, filename):
    
    # Create the meshgrid.
    
    fp = open(filename,'r')
    line1 = re.search(r'(\d+).+\s+([\d.]+),\s+([\d.]+)', fp.readline() )
    #print (line1)
    line2 = re.search(r'(\d+).+\s+([\d.]+),\s+([\d.]+)', fp.readline() )
    #print (line2)
    
    # x is multidimension x1=x, x2=y
    Nx = int(line1.group(1))
    #print ('Nx: ', Nx)
    Ny = int(line2.group(1))
    #print ('Ny: ', Ny)
    minx = float(line1.group(2))
    #print ('minx: ', minx)
    maxx = float(line1.group(3))
    #print ('maxx: ', maxx)
    miny = float(line2.group(2))
    #print ('miny: ', miny)
    maxy = float(line2.group(3))
    #print ('maxx: ', maxy)
    
    xyz = np.zeros((Nx,Ny,3))
    
    x = np.linspace(minx, maxx, Nx)
    #print ('x.shape: ', x.shape)
    #print (x[0])
    #print (x[-1])
    
    y = np.linspace(miny, maxy, Ny)
    #print ('y.shape: ', y.shape)
    #print (y[0])
    #print (y[-1])
    
    transformed_points = geodetic.transform_points(src_crs=proj_in, x=x, y=y)
    #print('transformed_points.shape: ' + str(transformed_points.shape))
    # print (transformed_points)
    lons = transformed_points[:, 0]
    #print_log('lons.shape: ' + str(lons.shape))
    #print (lons)

    lats = transformed_points[:, 1]
    #print_log('lats.shape: ' + str(lats.shape))
    #print (lats)

    X,Y = np.meshgrid(lons, lats)
    #print ('X.shape: ', X.shape)
    #print ('Y.shape: ', Y.shape)

    xyz[:,:,0] = X
    xyz[:,:,1] = Y

    z = np.loadtxt(filename, skiprows=3)
    #print ('z.shape: ', z.shape)
    xyz[:,:,2] = z
    #print (type(Z))
    #print (Z.shape)
    
    fp.close()
    
    return Nx, Ny, minx, maxx, miny, maxy, lons, lats, xyz

