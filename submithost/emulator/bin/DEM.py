#----------------------------------------------------------------------------------------------------------------------
# Class: DEM
# Component of: Titan2D Hazard Map Emulator Workflow
# Called from: Wrapper.py
# Purpose: Download a Shuttle Radar Topography Mission (SRTM) 30 m Global 1 arc second V0003 GeoTiff DEM
#          for the selected volcano and convert to GRASS GIS raster format for Titan2D.
# Author: Renette Jones-Ivey
# Date: Feb 2023
#---------------------------------------------------------------------------------------------------------------------
import sys
import numpy as np
import os
import time
import shutil
import tarfile

from Utils.deg2utm import deg2utm

# References:
# https://pypi.org/project/elevation/
# https://grasswiki.osgeo.org/wiki/GRASS_Python_Scripting_Library
# https://baharmon.github.io/python-in-grass

sys.path.append ('./elevation')
#print("sys.path: ", sys.path)

import elevation
#help (elevation)

# /usr/local/lib64/python3.6/site-packages/osgeo
from osgeo import gdal
#help(gdal)

from pyproj import CRS
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# For Unit Testing Only
Unit_Testing = False

#def main(argv):
def get_DEM(logger, self_workdir, volcano_lat_decimal_degrees, volcano_lon_decimal_degrees, \
         lat_south, lat_north, lon_west, lon_east,\
         grassgis_database, grassgis_location, grassgis_mapset, grassgis_map):
    
    #print ('DEM.py...')
    #print (argv)
    
    logger.info ('os.path.expanduser("~"): %s' %str(os.path.expanduser('~')))
    workingdir = os.getcwd()
    logger.info ('workingdir: %s' %workingdir)

    '''
    lat_south = float(argv[1])
    lat_north = float(argv[2])
    lon_west = float(argv[3])
    lon_east = float(argv[4])
    grassgis_database = os.path.join(workingdir, argv[5])
    grassgis_location = argv[6]
    grassgis_mapset = argv[7]
    grassgis_map = argv[8]
    '''
    
    if (0):
        print('volcano_lat_decimal_degrees: ', volcano_lat_decimal_degrees)
        print('volcano_lon_decimal_degrees: ', volcano_lon_decimal_degrees)
        print('lat_south: ', lat_south)
        print('lat_north : ', lat_north)
        print('lon_west: ', lon_west)
        print('lon_east: ', lon_east)
        print('grassgis_database: ', grassgis_database)
        print('grassgis_location ', grassgis_location)
        print('grassgis_mapset: ', grassgis_mapset)
        print('grassgis_map: ', grassgis_map)

    volcano_lon_utme, volcano_lat_utmn, utmzonen, utmzonel = deg2utm(volcano_lat_decimal_degrees, volcano_lon_decimal_degrees)

    if (0):
        print ('Latitude:', volcano_lat_utmn, '[UTMN]')
        print ('Longitude:', volcano_lon_utme, '[UMTE]')
        utmzone = '%02d%c' %(utmzonen,utmzonel)
        print('utmzone: %s' %utmzone)

    if np.sign(volcano_lat_decimal_degrees) == -1:
        utmzones = True
    else:
        utmzones = False
    logger.info('utmzones: %s' %utmzones)
    
    # Set GISBASE environment variable
    gisbase = '/usr/lib64/grass78'
    os.environ['GISBASE'] = gisbase
    logger.info ("os.environ['GISBASE']: %s" %str(os.environ['GISBASE']))
    
    # Set GISLOCK environment variable
    os.environ['GISLOCK'] = '$$'
    
    # define GRASS-Python environment
    grass_python_dir = os.path.join(gisbase, "etc", "python")
    logger.info ('grass_python_dir: %s' %grass_python_dir)
    sys.path.append(grass_python_dir)
    #print ('sys.path: ', sys.path)
    import grass.script as grass_script
    #help (grass)
    
    import grass.script.setup as grass_setup
    # Notes for setting up
    #help (grass_setup)
    
    #print ('Current GRASS 7 environment: ', grass_script.gisenv())
    
    start_time = time.time()
    
    # Geotiff has only 1 band
    geotiff1 = os.path.join(workingdir, 'elevation1.tif')
    #print ('geotiff1: ', geotiff1)
    geotiff2 = os.path.join(workingdir, 'elevation2.tif')
    #print ('geotiff2: ', geotiff2)
    geotiff3 = os.path.join(workingdir, 'elevation3.tif')
    #print ('geotiff3: ', geotiff3)
    geotiff4 = os.path.join(workingdir, 'elevation4.tif')
    #print ('geotiff4: ', geotiff4)
    
    #'''
    # clip the SRTM1 30m DEM and save it to elevation1.tif.
     
    # Example gdal_translate by elevation:
    # gdal_translate -q -co TILED=YES -co COMPRESS=DEFLATE -co ZLEVEL=9 -co PREDICTOR=2 -projwin -77.8 1.2 -77.56 0.96 SRTM1.5fa4addc81344a7bab06d2d24b420c22.vrt /user/renettej/GrassGIS/elevation1.tif 
    # Bounding box: left bottom right top
    elevation.clip(bounds=(lon_west, lat_south, lon_east, lat_north), output=geotiff1)
    # clean up stale temporary files and fix the cache in the event of a server error
    elevation.clean()
    #'''
    
    # elevation1.tif: Band 1 Block=256x256 Type=Int16, ColorInterp=Gray
    if (0):    
        print (gdal.Info(geotiff1))
    
    # Uncompress
    ds = gdal.Open(geotiff1)
    translate_options = gdal.TranslateOptions(format="GTiff", options=['COMPRESS=NONE'])
    ds = gdal.Translate(geotiff2, ds, options=translate_options)
    ds = None
    
    # elevation2.tif: Band 1 Block=864x4 Type=Int16, ColorInterp=Gray   
    if (0):    
        print (gdal.Info(geotiff2))
        
    # Translate to float
    ds = gdal.Open(geotiff2)
    ds = gdal.Translate(geotiff3, ds, outputType=gdal.GDT_Float32)
    ds = None
    
    # elevation3.tif: Band 1 Block=864x2 Type=Float32, ColorInterp=Gray    
    if (0):    
        print (gdal.Info(geotiff3))

    # Get the EPSG code
    crs = CRS.from_dict({'proj': 'utm', 'zone': int(utmzonen), 'south': utmzones})
    crs2 = crs.to_authority()
    #print (crs2)
    dst_crs = crs2[0]+':'+crs2[1]
    logger.info (dst_crs)

    # https://rasterio.readthedocs.io/en/stable/topics/reproject.html
    with rasterio.open(geotiff3) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs, 'transform': transform, 'width': width, 'height': height
            })
        
        with rasterio.open(geotiff4, 'w', **kwargs) as dst: 
            for i in range(1, src.count + 1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=dst_crs,
                        resampling=Resampling.nearest)    
    # elevation3.tif: Band 1 Block=864x2 Type=Float32, ColorInterp=Gray    
    if (0):    
        print (gdal.Info(geotiff4))            

    if os.path.exists(grassgis_database):
        #print ('removing: ', grassgis_database)
        shutil.rmtree(grassgis_database)
    os.mkdir(grassgis_database)
    #os.makedirs(database)

    #Create the rc file
    gisrc = grass_setup.init (gisbase, dbase=grassgis_database, location=grassgis_location, mapset=grassgis_mapset)
    f = open(gisrc,'r')
    output = f.read()
    f.close()
    if (0):    
        print ("os.environ['GISRC']: ", os.environ['GISRC'])
        print ('gisrc contents: ', output)
    
    #https://grass.osgeo.org/grass82/manuals/rasterintro.html
    env = grass_script.gisenv()
    
    env['GRASS_OVERWRITE'] = True
    env['GRASS_VERBOSE'] = True
    env['GRASS_MESSAGE_FORMAT'] = 'text'
    gisdbase = env['GISDBASE']
    location = env['LOCATION_NAME']
    mapset = env['MAPSET']
    #print ("os.environ['MAPSET']: ", os.environ['MAPSET'])
    
    os.environ['GRASS_COMPRESSOR'] = 'ZLIB'
    os.environ['GRASS_COMPRESS_NULLS'] = '1'

    if (0):    
        print ('env: ', env)
        print ('gisbase: ', gisdbase)
        print ('location: ', location)
        print ('mapset: ', mapset)
        print ('env: ', env)
        print ("os.environ['GRASS_COMPRESSOR']: ", os.environ['GRASS_COMPRESSOR'])
        print ("os.environ['GRASS_COMPRESS_NULLS']: ", os.environ['GRASS_COMPRESS_NULLS'])
        
    # OGR: vector data
    # GDAL: rastor data
    
    # This creates the PERMANENT mapset
    grass_script.run_command('g.proj', flags='ct', georef=geotiff4, location=grassgis_location)
    
    #print (grass_script.run_command('g.proj',flags='w')) #0
    
    # Print the current region in shell script style
    #print (grass_script.run_command('g.region', flags='p')) #0
    #print (grass_script.run_command('g.region', flags='g')) #0

    # Create the Grass GIS fcell raster file
    grass_script.run_command('r.in.gdal', input = geotiff4, output = grassgis_map, overwrite=True)
    
    grass_script.run_command('r.colors', map = grassgis_map, color = 'elevation')
    
    # list rasters in mapset
    #print('g.list: ', grass_script.run_command('g.list', type='rast', flags='p')) #0
    
    filepath = os.path.join(grassgis_database, grassgis_location, grassgis_mapset, 'cellhd', grassgis_map)
    logger.info ('\n%s:\n' %filepath)
    f = open(filepath, 'r')
    output = f.read()
    f.close()
    logger.info (output)
    
    #print (grass_script.run_command('r.compress', flags='p', map = grassgis_map)) #0

    #print (grass_script.run_command('g.proj', flags='p')) #0
      
    os.remove(gisrc)
    
    # Create tar file of the GRASS GIS database so Pegasus can uoload to Amazon S3,
    # the titan launch script will unzip it
    with tarfile.open(grassgis_database+".tar.gz", "w:gz") as tar:
        tar.add(grassgis_database, arcname=os.path.basename(grassgis_database))
    
    elapsed_time = time.time() - start_time
    #print ('elapsed time: ', np.round(elapsed_time/60.0, 2), ' [min]')
    
if Unit_Testing == True:
    
    # Azufral, Volcan
    workdir =  '~/AAA_Titan2D_Bayes_Linear_Method_Hazard_Map_Emulator_Workflow/submithost/emulator'
    volcano_lat_decimal_degrees =  1.08
    volcano_lon_decimal_degrees = -77.68
    lat_south = 0.96
    lat_north = 1.2
    lon_west = 77.8
    lon_east = -77.56
    grassgis_database = 'grassdata'
    grassgis_location = 'location'
    grassgis_mapset = 'PERMANENT'
    grassgis_map = 'map'
    
    get_DEM(workdir, volcano_lat_decimal_degrees, volcano_lon_decimal_degrees, \
        lat_south, lat_north, lon_west, lon_east, \
        grassgis_database, grassgis_location, grassgis_mapset, grassgis_map)
    
