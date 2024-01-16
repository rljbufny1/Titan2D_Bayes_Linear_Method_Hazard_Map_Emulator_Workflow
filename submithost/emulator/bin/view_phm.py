import os
from scipy import io
import numpy as np
#import pandas as pd
import matplotlib
# Do not display the plot
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Running with python version 3.6. Apparently with more recent version of python,
# pcolormesh(X,Y,C) with X(M,N), Y(M, N) and C (M,N,3), an image with RGB values (0-1 float),
# is allowed.
unit_test = 0

def rgb_to_decimal(r, g, b):
    rgb_decimal = r * 256 * 256 + g * 256 + b
    return rgb_decimal

def view_phm (workingdir):
    
    dd = io.loadmat('view_phm_data.mat')
    # Unit testing
    #print (type(dd))
    ca = dd['P_cvert2_reshaped']
    #print (ca.shape)
    cb = ca[0,:,:]
    #print (cb.shape)
    #cc = cb * 255.0
    cd = rgb_to_decimal(cb[:,0], cb[:,1], cb[:,2])
    #vmin = min(cd)
    #vmax = max(cd)
    #print ('vmin: %x' %int(vmin))
    #print ('vmax: %x' %int(vmax))
    #cd = cd/vmax
    #print (cd.shape)
    ss = int(np.sqrt(cd.shape[0]))
    #print (ss)
    global CP
    CP = cd.reshape(ss, ss)
    #print (type(C))
    #print (CP.shape)

    # M rows - y coordinates
    # N columns - x coordinates
    # X(M, N)
    xq = dd['X_quads']
    xf = np.sort(np.unique(xq.flatten()))
    #print (xf.shape)
    # Y(M,N)
    yq = dd['Y_quads']
    yf = np.sort(np.unique(yq.flatten()))
    #print (yf.shape)
    X, Y = np.meshgrid(np.linspace(xf[0],xf[-1],ss), np.linspace(yf[0],yf[-1],ss))
    #print (X.shape)
    #print (Y.shape)
    # Need to handle 4D
    #zq = dd['Z_quads']
    #print (type(zq))
    #print (zq.shape)
    # ca (M,N,3) an image with RGB values (0-1 float)
    
    fig, ax = plt.subplots()
    pf = plt.pcolormesh(X, Y, CP, cmap='gray', vmin=0.0, vmax=1.0)
    plt.colorbar(pf)
    ax.axis('scaled')
    ax.set_title('P(h>02[m])')
    ax.set_xlabel('East')
    ax.set_ylabel('North')
    plt.savefig(os.path.join(workingdir, 'P.png'))
    

    ca = dd['SDP_cvert2_reshaped']
    #print (ca.shape)
    cb = ca[0,:,:]
    #print (cb.shape)
    cc = cb * 255.0
    cd = rgb_to_decimal(cc[:,0], cc[:,1], cc[:,2])
    #vmin = min(cd)
    #vmax = max(cd)
    #cd = cd /vmax
    #print ('vmin: %x' %int(vmin))
    #print ('vmax: %x' %int(vmax))
    #print (cd.shape)
    ss = int(np.sqrt(cd.shape[0]))
    #print (ss)
    global CSDP
    CSDP = cd.reshape(ss, ss)
    #print (type(C))
    #print (C.shape)
    
    fig, ax = plt.subplots()
    pf = plt.pcolormesh(X, Y, CSDP, cmap='gray', vmin=0.0, vmax=1.0)
    plt.colorbar(pf)
    ax.axis('scaled')
    ax.set_title('SDP(h>02[m])')
    ax.set_xlabel('East')
    ax.set_ylabel('North')
    plt.savefig(os.path.join(workingdir, 'SDP.png'))

# Unit Testing 
if unit_test:
    view_phm ('.')


