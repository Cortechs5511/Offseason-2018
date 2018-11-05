import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class DriveStraightTime(TimedCommand):

    def __init__(self, speed = 0, timeout = 0):
        super().__init__('DriveStraightTime', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.speed = speed

    def execute(self):
        self.DT.tankDrive(self.speed,self.speed)

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
