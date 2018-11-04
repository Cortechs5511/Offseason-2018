import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from wpilib import SmartDashboard

class DriveStraightDistance(TimedCommand):

    def __init__(self, distance = 10, timeout = 0):
        super().__init__('DriveStraightDistance', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.setpoint = distance

    def initialize(self):
        setpoint = self.setpoint + self.DT.getAvgDistance()
        self.DT.setDistance(setpoint)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        rate = abs(self.DT.getAvgVelocity())
        minrate = 0.25

        if self.DT.distController.onTarget() and rate < minrate or self.isTimedOut(): return True
        else: return False

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
