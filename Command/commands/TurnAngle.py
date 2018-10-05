import math
import wpilib

from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class TurnAngle(TimedCommand):

    def __init__(self, angle = 0, timeout = 0):
        super().__init__('TurnAnglePID', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.angle = angle

    def initialize(self):
        self.DT.setAngle(self.angle)

    def isFinished(self):
        rate = abs(self.DT.getAvgAbsVelocity())
        minrate = 0.25

        if self.DT.distController.onTarget() and rate < minrate or self.isTimedOut(): return True
        else: return False

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
