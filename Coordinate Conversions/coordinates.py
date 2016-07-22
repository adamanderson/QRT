import numpy as np
#altaz to polar
def azel2polar(az, el):
    a = az*(np.pi/180)
    e = (el+0.1)*(np.pi/180)
    x = np.cos(a)*np.sin((np.pi/2)-e)
    z = np.cos((np.pi/2)-e)
    alpha = np.arccos(x)
    delta = np.arccos(z/(np.sin(np.arccos(x))))
    alphaindegs = alpha*(180/np.pi)
    deltaindegs = delta*(180/np.pi)
    print('Alpha=', alphaindegs)
    print('Delta=', deltaindegs)

#altaz to radec
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

#polar to altaz
def polar2altaz(alpha, delta): #needs to be in degrees
    #converts to radians
    d = delta*(np.pi/180)
    a = alpha*(np.pi/180)
    print(d)
    print(a)
    #converts to altaz
    az = np.arctan2(np.sin(a)*np.sin(d), np.cos(a))
    el = np.arctan2(np.sin(a)*np.cos(d), np.sqrt((np.cos(a)**2)+ (np.sin(a)**2)*(np.sin(d)**2)))
    azindeg = az*(180/np.pi)
    elindeg = el*(180/np.pi)
    
    print('Az=', azindeg)
    print('El=', elindeg)

#radec to altaz
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
