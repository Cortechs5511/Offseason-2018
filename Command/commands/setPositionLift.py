import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class setPositionLift(TimedCommand):

    def __init__(self, setpoint = 0, timeout = 300):
        super().__init__('setPositionLift', timeoutInSeconds = timeout)
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift
        self.setpoint = setpoint

    def initialize(self):
        self.Lift.setHeight(self.setpoint)

    def interrupted(self):
        self.end()

    def end(self):
        self.Lift.setSpeed(0)
