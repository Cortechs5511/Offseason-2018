import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class DriveStraightCombined(TimedCommand):

    def __init__(self, distance = 10, angle = 0, timeout = 0):
        super().__init__('DriveStraightCombined', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.distance = distance
        self.angle = angle

    def initialize(self):
        self.distance = self.distance + self.DT.getAvgDistance()
        self.DT.setCombined(distance=self.distance, angle=self.angle)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return (abs(self.distance-self.DT.getAvgDistance())<0.05 and self.DT.getAvgAbsVelocity()<0.05) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
