# QRTdaemon.py
#
# Main control daemon for running the QRT. The conceptual organization of the
# control software is this daemon is intended to always be running in the
# background and handles requests for telescope or DAQ activity via the Pyro
# module for remote object access. Using Pyro allows outside users to interact
# with the underlying motor control and DAQ modules through their native Python
# APIs, but simultaneously provides a persistance layer that allows these
# processes to live even if the network connection between the Raspberry Pi and
# a user's personal computer drops out. It also provides a natural mechanism for
# sharing data between the DAQ process and the motor control process without
# having to use more awkward Python tools for interprocess communication, or
# very painful low-level tools like sockets.
#
# Adam Anderson
# adama@fnal.gov
# 2016 July 3

import select
import sys
import Pyro4.core
import Pyro4.naming

import testcontrol


# boilerplate code to create pyro daemons
Pyro4.config.SERVERTYPE="thread"
print("initializing services... servertype=%s" % Pyro4.config.SERVERTYPE)
nameserverUri, nameserverDaemon, _ = Pyro4.naming.startNS(host='localhost') # use localhost for now, no broadcast server available
pyroDaemon=Pyro4.core.Daemon(host='localhost') # create a pyro daemon


# initialize objects whose data we intend to share via pyro
motorcontroller = testcontrol.DummyController()
# ... repeat as needed for other objects ...

# register the objects with the pyro daemon to get URI
motorcontroller_uri=pyroDaemon.register(motorcontroller)
# ... repeat as needed for other objects ...

# register URIs with the nameserver to allow lookup
nameserverDaemon.nameserver.register("motorcontroller.server",motorcontroller_uri)
# ... repeat as needed for other objects ...


# Core event loop
# This is always running in the background.
try:
    while True:
        # create sets of the socket objects we will be waiting on
        # (a set provides fast lookup compared to a list)
        nameserverSockets = set(nameserverDaemon.sockets)
        pyroSockets = set(pyroDaemon.sockets)
        rs = []
        rs.extend(nameserverSockets)
        rs.extend(pyroSockets)

        # wait for requests
        # (NB: 4th argument of select is a timeout length that effectively
        # throttles the speed of this loop)
        rs,_,_ = select.select(rs,[],[], 0.001)

        # handle requests
        eventsForNameserver=[]
        eventsForDaemon=[]
        for s in rs:
            if s in nameserverSockets:
                eventsForNameserver.append(s)
            elif s in pyroSockets:
                eventsForDaemon.append(s)
        if eventsForNameserver:
            nameserverDaemon.events(eventsForNameserver)
        if eventsForDaemon:
            pyroDaemon.events(eventsForDaemon)


        # do other regular tasks here...
        motorcontroller.increment_count()

except KeyboardInterrupt:
    # clean up
    nameserverDaemon.close()
    broadcastServer.close()
    pyrodaemon.close()
