import numpy as np
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

polar2altaz(49, 135)

