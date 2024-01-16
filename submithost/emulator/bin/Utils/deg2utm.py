def deg2utm(Lat,Lon):
    # -------------------------------------------------------------------------
    # https://www.mathworks.com/matlabcentral/fileexchange/10915-deg2utm?status=SUCCESS
    #
    # Copyright (c) 2006, Rafael Palacios
    # All rights reserved.
    #
    # deg2utm(Lat,Lon)
    #
    # Description: Function to convert lat/lon scalars into UTM coordinates (WGS84).
    # Some code has been extracted from UTM.m function by Gabriel Ruiz Martinez.
    #
    # Inputs:
    #    Lat [str]: Latitude.   Degrees.  +ddd.dddddd  WGS84
    #    Lon [str]: Longitude.  Degrees.  +ddd.dddddd  WGS84
    #
    # Outputs:
    #    utm.txt:
    #    x [utme], y [utmn], utmzone
    #
    # Author: 
    #   Rafael Palacios
    #   Universidad Pontificia Comillas
    #   Madrid, Spain
    # Version: Apr/06, Jun/06, Aug/06, Aug/06
    # Aug/06: fixed a problem (found by Rodolphe Dewarrat) related to southern 
    #    hemisphere coordinates. 
    # Aug/06: corrected m-Lint warnings.
    #   rlj
    #   Feb/23: Handle string scalar input.
    #   Mar/19: Convert to python.
    #-------------------------------------------------------------------------
    #https://mathesaurus.sourceforge.net/matlab-numpy.html
    import numpy as np
    
    # Argument checking
    #
    #error(nargchk(2, 2, nargin))  #2 arguments required
    
    la = float(Lat)
    #print('la: %.06f' %la)
    lo = float(Lon)
    #print('lo: %.06f' %lo)

    sa = 6378137.000000 
    sb = 6356752.314245

    #e = ( ( ( sa ^ 2 ) - ( sb ^ 2 ) ) ^ 0.5 ) / sa
    e2 = ( ( ( sa ** 2 ) - ( sb ** 2 ) ) ** 0.5 ) / sb
    e2cuadrada = e2 ** 2
    c = ( sa ** 2 ) / sb
    #alpha = ( sa - sb ) / sa             #f
    #ablandamiento = 1 / alpha   # 1/f

    lat = la * ( np.pi / 180 )
    lon = lo * ( np.pi / 180 )

    Huso = np.fix( ( lo / 6 ) + 31)
    S = ( ( Huso * 6 ) - 183 )
    deltaS = lon - ( S * ( np.pi / 180 ) )

    if (la<-72): Letra='C'
    elif (la<-64): Letra='D'
    elif (la<-56): Letra='E'
    elif (la<-48): Letra='F'
    elif (la<-40): Letra='G'
    elif (la<-32): Letra='H'
    elif (la<-24): Letra='J'
    elif (la<-16): Letra='K'
    elif (la<-8): Letra='L'
    elif (la<0): Letra='M'
    elif (la<8): Letra='N'
    elif (la<16): Letra='P'
    elif (la<24): Letra='Q'
    elif (la<32): Letra='R'
    elif (la<40): Letra='S'
    elif (la<48): Letra='T'
    elif (la<56): Letra='U'
    elif (la<64): Letra='V'
    elif (la<72): Letra='W'
    else: Letra='X'

    a = np.cos(lat) * np.sin(deltaS)
    epsilon = 0.5 * np.log( ( 1 +  a) / ( 1 - a ) )
    nu = np.arctan( np.tan(lat) / np.cos(deltaS) ) - lat
    v = ( c / ( ( 1 + ( e2cuadrada * ( np.cos(lat) ) ** 2 ) ) ) ** 0.5 ) * 0.9996
    ta = ( e2cuadrada / 2 ) * epsilon ** 2 * ( np.cos(lat) ) ** 2
    a1 = np.sin( 2 * lat )
    a2 = a1 * ( np.cos(lat) ) ** 2
    j2 = lat + ( a1 / 2 )
    j4 = ( ( 3 * j2 ) + a2 ) / 4
    j6 = ( ( 5 * j4 ) + ( a2 * ( np.cos(lat) ) ** 2) ) / 3
    alfa = ( 3 / 4 ) * e2cuadrada
    beta = ( 5 / 3 ) * alfa ** 2
    gamma = ( 35 / 27 ) * alfa ** 3
    Bm = 0.9996 * c * ( lat - alfa * j2 + beta * j4 - gamma * j6 )
    x = epsilon * v * ( 1 + ( ta / 3 ) ) + 500000
    y = nu * v * ( 1 + ta ) + Bm

    if (y<0):
       y=9999999+y
   
    return x, y, Huso, Letra


# Check.
# Also see: https://www.latlong.net/lat-long-utm.html
