from __future__ import print_function
import socket
import select
import sys
import Pyro4.core
import Pyro4.naming

import MotorControl

import timeit

Pyro4.config.SERVERTYPE="thread"
hostname=socket.gethostname()
print(hostname)

print("initializing services... servertype=%s" % Pyro4.config.SERVERTYPE)
# start a name server with broadcast server as well
nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host='localhost')
print(nameserverUri)
print(nameserverDaemon)

# create a Pyro daemon
pyrodaemon=Pyro4.core.Daemon(host='localhost')

# register a server object with the daemon
motorcontroller = MotorControl.MotorControl()
serveruri=pyrodaemon.register(motorcontroller)

# register it with the embedded nameserver directly
nameserverDaemon.nameserver.register("example.embedded.server",serveruri)

#testing
#nameserverDaemon.requestLoop()


# below is our custom event loop.
while True:
    start_time = timeit.default_timer()

    # create sets of the socket objects we will be waiting on
    # (a set provides fast lookup compared to a list)
    nameserverSockets = set(nameserverDaemon.sockets)
    pyroSockets = set(pyrodaemon.sockets)
    #rs=[broadcastServer]  # only the broadcast server is directly usable as a select() object
    rs = []
    rs.extend(nameserverSockets)
    rs.extend(pyroSockets)

    rs,_,_ = select.select(rs,[],[], 0.001)

    eventsForNameserver=[]
    eventsForDaemon=[]
    for s in rs:
        if s is broadcastServer:
            print("Broadcast server received a request")
            broadcastServer.processRequest()
        elif s in nameserverSockets:
            eventsForNameserver.append(s)
        elif s in pyroSockets:
            eventsForDaemon.append(s)
    if eventsForNameserver:
        print("Nameserver received a request")
        nameserverDaemon.events(eventsForNameserver)
    if eventsForDaemon:
        print("Daemon received a request")
        pyrodaemon.events(eventsForDaemon)
        elapsed = timeit.default_timer() - start_time
        print(elapsed)


    motorcontroller.increment_count()




nameserverDaemon.close()
broadcastServer.close()
pyrodaemon.close()
print("done")
