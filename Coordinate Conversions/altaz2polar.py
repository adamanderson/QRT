import numpy as np
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
azel2polar(180, 0)
