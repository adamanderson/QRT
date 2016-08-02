import sys
import Pyro4

ra = sys.argv[1]
dec = sys.argv[2]

function = sys.argv[3]

proxy = Pyro4.core.Proxy("PYRONAME:motorcontroller.server")
if(float(function) == 1):
    proxy.motorcontrol(float(ra), float(dec))
elif(float(function) == 2):
    proxy.reset()
elif(float(function) == 3):
    proxy.motorScan(float(ra), float(dec))
