def transform2deg(volcano_lat_decimal_degrees, volcano_lon_decimal_degrees):
    
    import numpy as np
    import cartopy.crs as ccrs

    from Utils.read_in_zgrid import read_in_zgrid
    from Utils.deg2utm import deg2utm

    # Titan2D creates elevation.grid and pileheightrecords in UTM coordinates.
    # Plotly express need WGS84 LL, ie. EPSG:4326.
    volcano_lon_utme, volcano_lat_utmn, utmzonen, utmzonel = deg2utm(
        volcano_lat_decimal_degrees, volcano_lon_decimal_degrees)
    
    print('Latitude:' + str(volcano_lat_utmn) +  ' [UTMN]')
    print('Longitude: ' + str(volcano_lon_utme) + ' [UMTE]')
    print('utmzonen: %s' % utmzonen)
    print('utmzonel: %s' % utmzonel)
    utmzone = '%02d%c' % (utmzonen, utmzonel)
    print('utmzone: %s' % utmzone)
    
    if np.sign(volcano_lat_decimal_degrees) == -1:
        utmzones = True
    else:
        utmzones = False
    print('utmzones: %s' % utmzones)
    
    # To convert coordinates from UTM to decimal degrees
    
    proj_in = ccrs.UTM(zone=int(utmzonen), southern_hemisphere=utmzones)
    #print('type(proj_in): ', type(proj_in))
    #print('proj_in: ', proj_in)
    
    # https://spatialreference.org/ref/epsg/
    #print('proj_in.to_epsg(): ', proj_in.to_epsg())
    #proj_out = ccrs.PlateCarree(central_longitude=0.0)
    # proj_out = ccrs.AzimuthalEquidistant()
    #print('type(proj_out): ', type(proj_out))
    #print('proj_out: ', proj_out)
    
    #proj_out_proj4 = proj_out.proj4_init
    #print('type(proj_out_proj4): ', type(proj_out_proj4))
    #print('proj_out_proj4: ', proj_out_proj4)
    
    # Transform projection
    geodetic = ccrs.Geodetic(globe=ccrs.Globe(ellipse='WGS84'))
    
    # Check
    # Returns transformed point with:
    # lon -180.0 to 180.0
    # lon -90.0 to 90.0
    transformed_point = geodetic.transform_point(
        src_crs=proj_in, x=volcano_lon_utme, y=volcano_lat_utmn)
    # print (transformed_point)
    volclon = transformed_point[0]
    volclat = transformed_point[1]
    #print('volclon: ' + str(volclon))
    #print('volclat: ' + str(volclat))

    '''
    transformed_points = geodetic.transform_points(src_crs=proj_in, x=x, y=y)
    print_log('transformed_points.shape: ' + str(transformed_points.shape))
    # print (transformed_points)
    lons = transformed_points[:, 0]
    #print_log('lons.shape: ' + str(lons.shape))
    #print (lons)

    lats = transformed_points[:, 1]
    #print_log('lats.shape: ' + str(lats.shape))
    #print (lats)
    '''
    
    return proj_in, geodetic
