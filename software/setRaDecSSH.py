import sys
import Pyro4

raH = sys.argv[1]
raM = sys.argv[2]
raS = sys.argv[3]
decH = sys.argv[4]
decM = sys.argv[5]
decS = sys.argv[6]

function = sys.argv[7]

raM += raS/60
raH += raM/60
decM += decS/60
decH += decM/60

proxy = Pyro4.core.Proxy("PYRONAME:motorcontroller.server")
if(float(function) == 1):
    proxy.motorcontrol(float(raH), float(decH))
elif(float(function) == 2):
    proxy.reset()
elif(float(function) == 3):
    proxy.motorScan(float(raH), float(decH))
