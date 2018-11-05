import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from wpilib import SmartDashboard

class setPositionWrist90(TimedCommand):

    def __init__(self, Debug = False, timeout = 0):
        super().__init__('setPositionWrist90', timeoutInSeconds = timeout)
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist

    def execute(self):
        angle = self.Wrist.getAngle()
        if angle > (math.pi / 4): self.Wrist.setSpeedNoG(0)
        else: self.Wrist.setSpeedNoG(0.55)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.Wrist.setSpeed(0)
