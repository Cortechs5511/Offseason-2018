import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class DriveStraightDistance(TimedCommand):

    def __init__(self, distance = 10, timeout = 0):
        super().__init__('DriveStraightDistance', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.setpoint = distance

    def initialize(self):
        self.setpoint = self.setpoint + self.DT.getAvgDistance()
        self.DT.setDistance(self.setpoint)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return (abs(self.setpoint-self.DT.getAvgDistance())<0.05 and self.DT.getAvgAbsVelocity()<0.05) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
