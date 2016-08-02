import sys
import Pyro4

ra = sys.argv[0]
dec = sys.argv[1]

function = sys.argv[2]

proxy = Pyro4.core.Proxy("PYRONAME:motorcontroller.server")
if(float(function) == 1):
    proxy.motorcontrol(float(ra), float(dec))
elif(float(function) == 2):
    proxy.reset()
elif(float(function) == 3):
    proxy.motorScan(float(ra), float(dec))
