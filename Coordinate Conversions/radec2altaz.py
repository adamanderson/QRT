import numpy as np
def radec2altaz(ra, dec, latitude, longitude, dj2000, ut): #needs to be in decimal form
    
    radegs = ra * 15 #turns ra from hours to degrees
    lst = 100.46 + 0.985647 * dj2000 + longitude + (15*ut)#gets the lst to use for later
    #while loops used to make lst in the range of 0-360
    
    while lst<0:
        lst += 360
        if lst>360:
            lst -= 360
    while lst>360:
        lst -= 360
        if lst<0:
            lst += 360
    #calculates the hour angle
    hourAngle = lst-radegs

    #while loops used to make hourAngle in the range of 0-360
    while hourAngle<0:
        hourAngle += 360
        if hourAngle>360:
            hourAngle -= 360
    while hourAngle>360:
        hourAngle -= 360
        if hourAngle<0:
            hourAngle += 360

    #puts all of the degree measurements into radians
    rightAscension = radegs*(np.pi/180)
    declination = dec*(np.pi/180)
    lat = latitude*(np.pi/180)
    longi = longitude*(np.pi/180)
    ha = hourAngle*(np.pi/180)
    
    #calculates the altitude and the azimuth
    sinALT = np.sin(declination)*np.sin(lat)+np.cos(declination)*np.cos(lat)*np.cos(ha)
    radALT = np.arcsin(sinALT)
    ALT = radALT*(180/np.pi)

    cosA = (np.sin(declination)-np.sin(radALT)*np.sin(lat))/(np.cos(radALT)*np.cos(lat))
    radA = np.arccos(cosA)
    A = radA*(180/np.pi)
    if np.sin(ha)<0: 
        AZ=A
    else:
        AZ=360-A
    
    print('Altitude=', ALT)
    print('Azimuth=', AZ)

radec2altaz(5.576, 20.015, 41.8383, -88.2616, 6016.3479, 20.35)
