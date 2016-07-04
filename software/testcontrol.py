# testcontrol.py
#
# Python module that defines a dummy class to show a.) how to define a class,
# and b.) how that class can be used by master_control.py to communicate with
# other processes.
#
# Adam Anderson
# adama@fnal.gov
# 2016 July 3

class DummyController(object):
    def __init__(self):
        self.switches = 0

    def get_count(self):
        return self.switches

    def increment_count(self):
        self.switches = self.switches + 1
