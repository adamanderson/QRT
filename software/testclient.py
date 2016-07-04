# testclient.py
#
# An example "client" script to demonstrate how to use pyro to access an object
# within another process.
#
# Adam Anderson
# adama@fnal.gov
# 2016 July 3

from __future__ import print_function
import Pyro4

proxy=Pyro4.core.Proxy("PYRONAME:motorcontroller.server")
print("count = %d" % proxy.get_count())
