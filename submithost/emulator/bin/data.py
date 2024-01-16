#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 15:57:07 2022

@author: renettej
"""
import os
import numpy as np
#import numpy.ma as ma
#import math
#import scipy.integrate as integrate
import matplotlib
#non-interactive backend that can only write to files
# This sets it for all code
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D    ni = 48


import time
from read_in_zgrid import read_in_zgrid
import pandas as pd

cmap = "RdBu_r" #cm.jet

def get_data(datadir, volcano_lon_utme, volcano_lat_utmn, minvol, maxvol, minbed, maxbed, h, radius, maxN):
    
    #'''
    ni = 48
    Xtest = np.zeros((ni, 5))
    margin = .05
    #h = 1389.5
    h_min = h - h * margin
    h_max = h + h * margin
    Xtest[:,0] = np.linspace ( h_min, h_max, ni )
    #radius = 1389.5
    radius_min =  radius - radius * margin
    radius_max =  radius - radius * margin
    Xtest[:,1] = np.linspace ( radius_min, radius_max, ni )
    # x, longitude is UTME aka degrees east -180 to 180
    #UTME = 197440.06
    UTME_min = volcano_lon_utme - volcano_lon_utme * margin
    UTME_max = volcano_lon_utme + volcano_lon_utme * margin
    # y, latitude is UTMN aka degrees north  -90 to 90
    Xtest[:,2] = np.linspace ( UTME_min, UTME_max, ni )
    #UTMN = 120005.02
    UTMN_min = volcano_lat_utmn - volcano_lat_utmn * margin
    UTMN_max = volcano_lat_utmn + volcano_lat_utmn * margin
    Xtest[:,3] = np.linspace ( UTMN_min, UTMN_max, ni )
    bedfric_min = minbed - minbed * margin
    bedfric_max = maxbed - maxbed * margin
    Xtest[:,4] = np.linspace ( bedfric_min, bedfric_max, ni )
    print ('Xtest.shape: ', Xtest.shape)
    #'''
    
    # Normalize the data
    for i in range(Xtest.shape[1]):
        print (np.std(Xtest[:,i]))
        Xtest[:,i] = (Xtest[:,i] - np.mean(Xtest[:,i])) / np.std(Xtest[:,i])
        
    # Xtrain

    filename = os.path.join(datadir, 'uncertain_input_list_h.txt')
    dataset = pd.read_csv(filename,index_col=None,skiprows=6,\
        names=['h','radius','UTME','UTMN','bedfric'],\
        delim_whitespace='True',\
        #on_bad_lines='warn',\
        engine='python')
    print (type(dataset))
    #print (dataset)
      
    data = np.array(dataset)
    print ('data.shape: ', data.shape)
    #print (data)
    
    samples = data.shape[0]
    print ('samples: ', samples)
    
    # Normalize the data
    for i in range(data.shape[1]):
        print (np.std(data[:,i]))
        data[:,i] = (data[:,i] - np.mean(data[:,i])) / np.std(data[:,i])
    #print (data)
    
    Xtrain = data
    print ('Xtrain.shape: ', Xtrain.shape)
    
    # Normalize the data
    for i in range(Xtrain.shape[1]):
        print (np.std(Xtrain[:,i]))
        Xtrain[:,i] = (Xtrain[:,i] - np.mean(Xtrain[:,i])) / np.std(Xtrain[:,i])

    # Samples
    
    s = time.time()
    filename = os.path.join(datadir, 'LOCAL/shared-storage/pileheightrecord.%06d' %1)
    Nx, Ny, minx, maxx, miny, maxy, gridx, gridy, xyz = read_in_zgrid(filename, maxN) 
    print ('Nx: ', Nx)  
    print ('Ny: ', Ny)  
    #print ('xyz.shape: ', xyz.shape)
    print (time.time() - s)
    
    samples_x = np.zeros((samples, Nx, Ny))
    samples_y = np.zeros((samples, Nx, Ny))
    samples_z = np.zeros((samples, Nx, Ny))
    s = time.time()
    for i in range(samples):
        filename = os.path.join(datadir, 'LOCAL/shared-storage/pileheightrecord.%06d' %(i+1))
        Nx, Ny, minx, maxx, miny, maxy, gridx, gridy, xyz = read_in_zgrid(filename, maxN)   
        #print ('Nx: ', Nx)  
        #print ('Ny: ', Ny)  
        samples_x[i,:,:] = xyz[:,:,0]
        samples_y[i,:,:] = xyz[:,:,1]
        samples_z[i,:,:] = xyz[:,:,2]
    print (time.time() - s)
    
    max_samples_z1 = np.zeros((samples,2))
    for i in range(samples):
        max_samples_z1[i,0] = i
        max_samples_z1[i,1] = np.max(samples_z[i,:,:])
    #print (max_samples_z1)
    # Sort by second column
    ind=np.argsort(max_samples_z1[:,-1])
    sorted1=max_samples_z1[ind]
    #print (sorted1)
    # Reverse order
    sorted2=sorted1[::-1]
    #print(sorted2)
    
    if (0):
        
        rows = 8
        cols = int(samples/rows)
        fig, ax = plt.subplots(rows, cols, figsize=(20,20))
        #print (ax)
        i = 0
        s = time.time()
        for j in range(rows):
            for k in range(cols):
                cs = ax[j,k].contour(samples_x[i,:,:], samples_y[i,:,:], samples_z[i,:,:], cmap=cmap)
                #ax[j,k].set_title('P')
                #ax[j,k].set_xlabel('East')
                #ax[j,k].set_ylabel('North')
                fig.colorbar(cs, ax=ax[j,k])
                #cbar.ax.set_ylabel('Pile Height')
                i = i + 1
    else:
        
        rows = 3
        cols = 2
        fig, ax = plt.subplots(rows, cols, figsize=(20,20))
        #print (ax)
        s = time.time()
        i = 0
        for j in range(rows):
            for k in range(cols):
                idx = int(sorted2[i,0])
                #print (idx)
                cs = ax[j,k].contour(samples_x[idx,:,:], samples_y[idx,:,:], samples_z[idx,:,:], cmap=cmap)
                #ax[j,k].set_title('P')
                #ax[j,k].set_xlabel('East')
                #ax[j,k].set_ylabel('North')
                fig.colorbar(cs, ax=ax[j,k])
                #cbar.ax.set_ylabel('Pile Height')
                i = i + 1
    #plt.show()
    plt.savefig('pileheights_raw.png')
    
    return Xtest, Xtrain, samples_x, samples_y, samples_z
