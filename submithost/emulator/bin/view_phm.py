#----------------------------------------------------------------------------------------------------------------------
# Component of: Titan2D Hazard Map Emulator Workflow
# Purpose: Create hazrad map images
# Called from: emulator.ipynb
# Author: Renette Jones-Ivey
# Date: Apr 1024
#---------------------------------------------------------------------------------------------------------------------

# References:
# https://github.com/holoviz/datashader

#from bokeh.plotting import show
from colorcet import fire, rainbow4, kb
#import datashader as ds
from datashader.transfer_functions import shade
#import datashader.transfer_functions as tf
#from datashader.colors import Elevation
#from datashader.utils import export_image
from datashader.transfer_functions import stack
#import geopandas as geopd
#import holoviews as hv
import datetime
import numpy as np
import os
#import pandas as pd
# https://plotly.github.io/plotly.py-docs/plotly.express.html
#import plotly.express as px
#import rioxarray
from scipy.interpolate import NearestNDInterpolator
import sys
import time
import xarray as xr
from xrspatial import hillshade
import matplotlib
from matplotlib import cm, colors
import matplotlib.pyplot as plt
#import numpy as np
#import matplotlib.pyplot as plt

#print ('sys.path: ', sys.path)
from Utils.read_in_zgrid import read_in_zgrid
from Utils.transform2deg import transform2deg

import ipywidgets as widgets
from IPython.display import display, HTML, Markdown, clear_output, Javascript, IFrame

Unit_Test = False

if Unit_Test == False:
    # plt.savefig - do not display the image
    matplotlib.use('Agg')

def print_log (message):
    print (message)
    
def get_phm(proj_in, geodetic, hazmapfilename):

    global EAST
    global NORTH
    global x
    global lons
    global y
    global lats
    global transformed_points
    global z
    global P
    global ldiff
    global XMAPWIWI2

    with open(hazmapfilename, 'r') as fid:

        line = fid.readline()
        #print('line: ', line)

        #print("line.split('='): ", line.split('='))

        Nskip = int(line.split('=')[1])
        #print ('Nskip: ', Nskip)

        for i in range(Nskip):
            line = fid.readline()
            #print ('line: ', line)
        crith = float(fid.readline().split()[0])
        #print_log('crith: ' + str(crith))
        Ndiminmacro = int(fid.readline().split()[0])
        #print_log('Ndiminmacro: ' + str(Ndiminmacro))
        W = float(fid.readline().split()[0])
        #print_log('W: ' + str(W))
        Nxmap = int(fid.readline().split()[0])
        #print_log('Nxmap: ' + str(Nxmap))
        XMAPWIWI2 = np.array(
            [list(map(float, fid.readline().split())) for _ in range(Nxmap)])
        Nresamp = int(fid.readline().split()[0])
        #print ('Nresamp: ', Nresamp)
        XMACROw = np.array(
            [list(map(float, fid.readline().split())) for _ in range(Nresamp)])

    x = XMAPWIWI2[0:Nxmap, 0]
    y = XMAPWIWI2[0:Nxmap, 1]

    # https://scitools.org.uk/cartopy/docs/v0.14/crs/index.html
    transformed_points = geodetic.transform_points(src_crs=proj_in, x=x, y=y)
    #print('transformed_points.shape: ', transformed_points.shape)
    # print (transformed_points)
    lons = transformed_points[:, 0]
    #print('lons.shape: ', lons.shape)
    #print (lons)

    lats = transformed_points[:, 1]
    #print('lats.shape: ', lats.shape)
    #print (lats)

    # For the P map
    P = XMAPWIWI2[:, 2] / W
    # For the (sigma P) / P map (sigma divided by P)
    SDP = np.sqrt((XMAPWIWI2[:, 3] / Nresamp - XMAPWIWI2[:, 2] ** 2 / Nresamp ** 2) * (Nresamp ** 3 / ((Nresamp - 1) * W ** 2)) / Nresamp)

    #izero = np.where((~SDP) & (~P))[0]
    # P[izero] = np.nan
    #SDP[izero] = np.nan

    #minx, maxx = min(lons), max(lons)
    #xminmax = [minx, maxx]
    #miny, maxy = min(lats), max(lats)
    #yminmax = [miny, maxy]

    diff = enumerate(np.diff(lats))
    ldiff = list(diff)
    NEAST = next(i for i, x in enumerate(np.diff(y)) if x != 0) + 1
    #print('NEAST: ', NEAST)
    # // is floor
    NNORTH = Nxmap // NEAST
    #print('NNORTH: ', NNORTH)
    EAST = lons.reshape(NEAST, NNORTH, order='F')
    NORTH = lats.reshape(NEAST, NNORTH, order='F')
    P = P.reshape(NEAST, NNORTH, order='F')
    #print('P.shape: ', P.shape)
    SDP = SDP.reshape(NEAST, NNORTH, order='F')
    #print('SDP.shape: ', SDP.shape)

    # return EAST, NORTH, P, SDP, xminmax, yminmax
    # https://stackoverflow.com/questions/38064697/interpolating-a-numpy-array-to-fit-another-array
    z = P
    #print('z.shape: ', z.shape)
    #z = np.ma.masked_where(z == 0.0, z)
    #print ('z: ', z)

    return crith, EAST, NORTH, P, SDP


def view_phm (workingdir, resultsdir, volcname, volcano_lat_decimal_degrees, volcano_lon_decimal_degrees):
    
    global xyz
    
    #print_log('Volcano Name: ' + str(volcname))
    
    #print_log('volcano_lat_decimal_degrees: ' +
          #str(volcano_lat_decimal_degrees) + ' [Decimal Degrees]')
    #print_log('volcano_lon_decimal_degrees: ' +
          #str(volcano_lon_decimal_degrees) + ' [Decimal Degrees]')
        
    #start_time = time.time()
    latitude = "%s [degrees north -90 to 90]" %str(volcano_lat_decimal_degrees)
    longitude = "%s [degrees east -180 to 180]" %str(volcano_lon_decimal_degrees)

    proj_in, geodetic = transform2deg (volcano_lat_decimal_degrees, volcano_lon_decimal_degrees)
 
    filename = os.path.join(resultsdir, 'elevation.grid')
    Nx, Ny, minx, maxx, miny, maxy, gridx, gridy, xyz = read_in_zgrid(proj_in, geodetic, filename)
    glon = gridx
    glat = gridy
    gz = xyz[:, :, 2]
    #print('glon.shape: ', glon.shape)
    #print('glat.shape: ', glat.shape)
    #print('gz.shape: ', gz.shape)
    
    hazmapfilename = os.path.join(resultsdir, 'AZ_vol_dir_bed_int_final.phm')
    crith, EAST, NORTH, P, SDP = get_phm(proj_in, geodetic, hazmapfilename)
    #print('EAST.shape: ', EAST.shape)
    #print('NORTH.shape: ', NORTH.shape)
    #print('P.shape: ', P.shape)
    #print('SDP.shape: ', SDP.shape)

    X, Y = np.meshgrid(glon, glat)
    #print('X.shape: ', X.shape)
    #print('Y.shape: ', Y.shape)
    
    #unique = np.unique(P)
    #print('unique.shape: ', unique.shape)
    #print ('unique: ', unique)
    
    x = np.array(list(zip(EAST.flatten(), NORTH.flatten())))
    interp = NearestNDInterpolator(x=x, y=P.flatten())
    iP = interp(X, Y)
    #print('x.shape: ', x.shape)
    #print('type(ipz): ', type(ipz))
    #print('ipz.shape: ', ipz.shape)
    #unique = np.unique(iP)
    #print('unique.shape: ', unique.shape)
    #print ('unique: ', unique)
    iP = np.ma.masked_where(iP == 0.0, iP)
    
    interp = NearestNDInterpolator(x=x, y=SDP.flatten())
    iSDP = interp(X, Y)
    #print('x.shape: ', x.shape)
    #print('type(ipz): ', type(ipz))
    #print('ipz.shape: ', ipz.shape)
    #unique = np.unique(iSDP)
    #print('unique.shape: ', unique.shape)
    #print ('unique: ', unique)
    iSDP = np.ma.masked_where(iSDP == 0.0, iSDP)

    
    '''
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(X.ravel(), Y.ravel(), ipz.ravel(),
               s=10, c='r', label='data')
    '''
    grid_dem = xr.DataArray(gz, coords=[glon, glat], dims=['lon', 'lat'])
    grid_dem.attrs = dict(
        AREA_OR_POINT="Area",
        scale_factor="1.0",
        add_offset="0.0",
    )
    #print ('grid_dem: ', grid_dem)
    
    
    P_dem = xr.DataArray(iP, coords=[glon, glat], dims=['lon', 'lat'])
    P_dem.attrs = dict(
        AREA_OR_POINT="Area",
        scale_factor="1.0",
        add_offset="0.0",
    )
    #print ('P_dem: ', P_dem)
    
    SDP_dem = xr.DataArray(iSDP, coords=[glon, glat], dims=['lon', 'lat'])
    SDP_dem.attrs = dict(
        AREA_OR_POINT="Area",
        scale_factor="1.0",
        add_offset="0.0",
    )
    #print ('P_dem: ', P_dem)

    
    #elevation = shade(grid_dem, cmap=Elevation, how='linear')
    # print ('type(elevation): ', type(elevation))  #<class 'datashader.transfer_functions.Image'>
    # print ('type(elevation.to_pil()): ', type(elevation.to_pil())) #<class 'PIL.Image.Image'>
    '''
    fig, ax = plt.subplots()
    plt.imshow(elevation.to_pil(), extent=[glon[0],glon[-1],glat[0],glat[-1]])
    '''
    #export_image(img=elevation, filename='test1', fmt=".png",  export_path=".")
    
    illumination = hillshade(grid_dem)
    # print ('type(illumination: ', type(illumination)) #<class 'xarray.core.dataarray.DataArray'>
    
    hillshade_gray = shade(illumination, cmap=[
                           'gray', 'white'], alpha=255, how='linear')
    #print ('type(hillshade_gray): ', type(hillshade_gray))
    '''
    fig, ax = plt.subplots()
    plt.imshow(hillshade_gray.to_pil(), extent=[glon[0],glon[-1],glat[0],glat[-1]])
    '''
    #export_image(img=hillshade_gray, filename='test2', fmt=".png",  export_path=".")
    
    phm = shade(P_dem, cmap=cm.jet, alpha=128, how='linear')
    #phm = shade(P_dem, cmap=fire, alpha=128, how='linear')
    #phm = shade(P_dem, cmap=rainbow4, alpha=128, how='linear')
    # plt.imshow(phm.to_pil())
    
    stacked = stack(hillshade_gray, phm)
    #print ('type(stacked): ', type(stacked))
    #plt.title ('P > %.2f [m]' %crith, fontsize=14, fontweight='demibold')
    #fig, ax = plt.subplots()
    
    # Display title page
    header = 'Hazard Report'
    utc_now = datetime.datetime.utcnow()
    utc_now = str(datetime.datetime(utc_now.year, utc_now.month, utc_now.day, utc_now.hour, utc_now.minute, utc_now.second))

    display(Markdown('# <center>'+header))
    display(Markdown('# <center> '))
    display(Markdown('### <left> Date/Time UTC: %s' %utc_now))
    display(Markdown('### <left> Volcano Name: %s' %volcname))
    display(Markdown('### <left> Latitude: %s' %latitude))
    display(Markdown('### <left> Longitude: %s' %longitude))
    display(Markdown('# <center> '))

    # '''
    fig, ax = plt.subplots(figsize=(8, 8))#, layout='constrained')
    plt.imshow(stacked.to_pil(), extent=[glon[0], glon[-1], glat[0], glat[-1]])
    ax.set_title('%s\n P(h>%.2f[m])' % (volcname, crith), fontsize = 14)
    ax.set_xlabel('East')
    ax.set_ylabel('North')
    #https://colorcet.holoviz.org/user_guide/Continuous.html
    cmap = cm.jet
    #cmap = 'cet_CET_L3' # fire
    #cmap = 'cet_CET_R4' # rainbow4
    # TypeError is returned: You must first set_array for mappable
    norm = cm.ScalarMappable(norm=colors.Normalize(vmin=0,vmax=1), cmap=cmap)
    norm.set_array([])
    fig.colorbar(norm, ax=ax, orientation='vertical', fraction=0.0425, pad=0.04)
    #norm = colors.Normalize(vmin=0,vmax=1)
    #cbar = colorbar.ColorbarBase(ax=ax, cmap=cmap, norm=norm, orientation='vertical')
    plt.savefig(os.path.join(resultsdir, 'P.png'))
    # '''
    #image = np.array(stacked.to_pil())
    #print ('image.shape: ', image.shape)
    
    phm = shade(SDP_dem, cmap=kb, alpha=128, how='linear')
    # plt.imshow(phm.to_pil())
    
    stacked = stack(hillshade_gray, phm)
    #print ('type(stacked): ', type(stacked))
    #plt.title ('P > %.2f [m]' %crith, fontsize=14, fontweight='demibold')
    #fig, ax = plt.subplots()
    # '''
    fig, ax = plt.subplots(figsize=(8, 8))#, layout='constrained')
    plt.imshow(stacked.to_pil(), extent=[glon[0], glon[-1], glat[0], glat[-1]])
    ax.set_title('%s\n SDP(h>%.2f[m])' % (volcname, crith), fontsize = 14)
    ax.set_xlabel('East')
    ax.set_ylabel('North')
    #https://colorcet.holoviz.org/user_guide/Continuous.html
    cmap = 'cet_CET_L15' # kb
    # TypeError is returned: You must first set_array for mappable
    norm = cm.ScalarMappable(norm=colors.Normalize(vmin=0,vmax=1), cmap=cmap)
    norm.set_array([])
    fig.colorbar(norm, ax=ax, orientation='vertical', fraction=0.0425, pad=0.04)
    #norm = colors.Normalize(vmin=0,vmax=1)
    #cbar = colorbar.ColorbarBase(ax=ax, cmap=cmap, norm=norm, orientation='vertical')
    plt.savefig(os.path.join(resultsdir, 'SDP.png'))
    # '''
    #image = np.array(stacked.to_pil())
    #print ('image.shape: ', image.shape)
    
    # Create report
    import matplotlib.backends.backend_pdf
    from PIL import Image as PIL_image
    pdffilepath = os.path.join(resultsdir, 'Hazard_Report.pdf')
    pdf = matplotlib.backends.backend_pdf.PdfPages(pdffilepath)

    # Fig and settings for the PDF
    fig = plt.figure()
    plt.axis('off')
    plt.text(.5, .9, header+'\n\n', va='top', ha='center', fontsize=12, fontweight='bold', wrap=False)
    plt.text(.1, .64, 'Date/Time UTC: %s' %utc_now, va='top', ha='left', fontsize=10, fontweight='bold', wrap=False)
    plt.text(.1, .58, 'Volcano Name: %s' %volcname, va='top', ha='left', fontsize=10, fontweight='bold', wrap=False)
    plt.text(.1, .52, 'Latitude: %s' %latitude, va='top', ha='left', fontsize=10, fontweight='bold', wrap=False)
    plt.text(.1, .46, 'Longitude: %s' %longitude, va='top', ha='left', fontsize=10, fontweight='bold', wrap=False)
    pdf.savefig(fig)
    plt.close()

    figures = [os.path.join(resultsdir, 'P.png'), os.path.join(resultsdir, 'SDP.png')]
    num_figures = 2
    
    for i in range(num_figures):

        figure = figures[i]
        #print ('figure: ', figure)
        figure_basename = os.path.basename(figure)
        #print ('figure_basename: ', figure_basename)
        #figure_name = figure_basename[0:-4]
        #print ('figure_name: ', figure_name)
        figure_title = figure_basename
        
        figure_caption = 'fig. %d' %(i+1)
        
        image = PIL_image.open(figure) #plt_image.imread(figure)
        #print ('type(image): ', type(image)) #<class 'PIL.PngImagePlugin.PngImageFile'>
        
        # Fig and settings for the PDF
        fig = plt.figure(figsize=(50, 50))
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        #print ('ax.axis: ', ax.axis()) #(0.0, 1.0, 0.0, 1.0)
        xmin, xmax, ymin, ymax = ax.axis()
        
        ax.imshow(image)
        ax.text(.5, ymax + .05, figure_title+'\n\n', va='top', ha='center', fontsize=70, fontweight='bold', wrap=False, transform=ax.transAxes)
        ax.text(.5, ymin - .105, figure_caption+'\n\n', va='bottom', ha='center', fontsize=70, fontweight='bold', wrap=False, transform=ax.transAxes)
        pdf.savefig(fig)
        plt.close()
    
    pdf.close()
    #print('Elapsed time: ' + str(time.time() - start_time))


# Unit Testing 
if Unit_Test:
    
    # Add to PYTHONPATH
    #sys.path.append('.')
    
    volcname = 'COLIMA VOLC COMPLEX'
    volcano_lat_decimal_degrees = 19.514
    volcano_lon_decimal_degrees = -103.62

    view_phm ( '.', '../LOCAL_COLIMA VOLC COMPLEX/shared-storage', volcname, volcano_lat_decimal_degrees, volcano_lon_decimal_degrees)


