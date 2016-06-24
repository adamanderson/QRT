class MotorControl(object):
    def __init__(self):
        self.switches = 0

    def get_count(self):
        return self.switches

    def increment_count(self):
        self.switches = self.switches + 1
