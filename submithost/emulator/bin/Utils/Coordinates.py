#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Feb 2023

@author: renettej
"""

import numpy as np
import cartopy.crs as ccrs

# http://vikas-ke-funde.blogspot.com/2010/06/convert-longitude-0-360-to-180-to-180.htmldef
# https://apollomapping.com/blog/gtm-finding-a-utm-zone-number-easily

# From volcashexpwf:
# Using the PlateCarree projection. See https://scitools.org.uk/cartopy/docs/latest/reference/projections.html
# When lon[0] is E (+) and lon[-1] is W (-), for example near the 180th meridian,
# plot does not display properly when central_longitude == 0.0
#if lon[-1] < lon[0]:
    #proj_in = ccrs.PlateCarree(central_longitude = 180.0)
    #proj_out = ccrs.PlateCarree(central_longitude = 180.0)
#else:
    #proj_in = ccrs.PlateCarree(central_longitude = 0.0)
    #proj_out = ccrs.PlateCarree(central_longitude = 0.0)


class Convert():

    def __init__(self):
        pass
        
    # Convert longitude from (-180 to 80) to (0-360)      
    def convert_lon_minus180_180_to_0_360(self, degree_minus180_180 ):
        
        degree_0_360 = degree_minus180_180  % 360.0   
        return degree_0_360
    
    # Convert longitude from (0-360) to (-180 to 80)        
    def convert_lon_0_360_to_minus180_180(self, degree_0_360):
        
        degree_minus180_180 = ((degree_0_360 + 180.0) % 360.0) - 180.0
        return degree_minus180_180
    
    # Convert from decimal degrees to UTM
    
    def convert_from_decimal_degrees_to_utm(self, lat_decimal_degrees, lon_decimal_degrees):
        
        # To verify:
        #https://www.latlong.net/lat-long-utm.html
        
        # Returns transformed point with: 
        # lon -180.0 to 180.0
        # lon -90.0 to 90.0
        # How does this change depending on location
        proj_in = ccrs.PlateCarree(central_longitude = 0.0)
        #print ('type(proj_in): ', type(proj_in))
        #print ('proj_in: ', proj_in)
        
        utm_zone = int(np.ceil((lon_decimal_degrees + 180.0) / 6.0))
        if lat_decimal_degrees < 0.0:
            south = True
        else:
            south = False
        print ('UTM Zone: ', utm_zone)
        print ('Southern Hemisphere: ', south)
        proj_out = ccrs.UTM(zone=utm_zone, southern_hemisphere=south)
        
        #print ('type(proj_out): ', type(proj_out))
        #print ('proj_out: ', proj_out)
        
        transformed_point = \
            proj_out.transform_point(src_crs=proj_in, x=lon_decimal_degrees, y=lat_decimal_degrees)
        #print ('transformed_point: ', transformed_point)
        
        return (transformed_point)
    
#if __name__ == "__main__":
  #main()
