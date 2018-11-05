import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from wpilib import SmartDashboard

class setPositionLift(TimedCommand):

    def __init__(self, setpoint = 0, Debug = False, timeout = 300):
        super().__init__('setPositionLift', timeoutInSeconds = timeout)
        self.setpoint = setpoint
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift

    def initialize(self):
        self.Lift.setHeight(self.setpoint)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.Lift.setSpeed(0)
