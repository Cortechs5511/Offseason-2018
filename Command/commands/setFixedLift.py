import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class setFixedLift(TimedCommand):

    def __init__(self, speed = 0, timeout = 0):
        super().__init__('setFixedLift', timeoutInSeconds = timeout)
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift
        self.speed = speed

    def execute(self):
        self.Lift.setSpeed(self.speed)

    def interrupted(self):
        self.end()

    def end(self):
        self.Lift.setSpeed(0)
