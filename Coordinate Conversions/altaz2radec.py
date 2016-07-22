import numpy as np
def altaz2radec(altitude, azimuth, latitude, longitude, time, dj2000): #needs to be in degrees
    #converts from degrees to radians
    alt = altitude*(np.pi/180)
    az = azimuth*(np.pi/180)
    lat = latitude*(np.pi/180)
    #calculates declination and hour angle
    dec = np.arcsin(np.sin(lat)*np.sin(alt)+np.cos(lat)*np.cos(alt)*np.cos(az))
    ha = np.arccos((np.sin(alt)-np.sin(dec)*np.sin(lat))/(np.cos(dec)*np.cos(lat)))
    haindegs = ha*(180/np.pi)#converts hour angle from radians to degrees
    lst = 100.46 + 0.985647 * dj2000 + longitude + (15*time) #calculates lst
    #makes sure the lst is between 0 and 360
    while lst<0:
        lst += 360
        if lst>360:
            lst -= 360
    while lst>360:
        lst -= 360
        if lst<0:
            lst += 360
    ra = lst-haindegs #calculates right ascension
    rainhours = ra/15 #converts right ascension from degrees to hours
    decindegs = dec*(180/np.pi)#converts declination radians to degrees
    print('RA=',rainhours)
    print('DEC=',decindegs)
altaz2radec(49.05, 254.69, 41.8383, -88.2616, 20.35, 6016.3479)
