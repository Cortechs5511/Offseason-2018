import math
import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand

class DriveStraightTimePID(TimedCommand):

    def __init__(self,speed = 0, timeout = 0):
        super().__init__('DriveStraightTimePID', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.speed = speed

    def execute(self):
        LeftSpeed = self.speed + err
        RightSpeed = self.speed - err
        self.DT.tankDrive(LeftSpeed,RightSpeed)

    def interrupted(self):
        self.end()

    def isFinished(self):
         return self.isTimedOut()

    def end(self):
        self.DT.tankDrive(0,0)
