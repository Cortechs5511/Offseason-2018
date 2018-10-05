import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class setFixedDT(TimedCommand):

    def __init__(self, leftSpeed = 0, rightSpeed = 0, timeout = 300):
        super().__init__('setFixedDT', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.leftSpeed = leftSpeed
        self.rightSpeed = rightSpeed

    def execute(self):
        self.DT.tankDrive(self.leftSpeed,self.rightSpeed)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
