from __future__ import print_function
import Pyro4

proxy=Pyro4.core.Proxy("PYRONAME:example.embedded.server")
print("count = %d" % proxy.get_count())
