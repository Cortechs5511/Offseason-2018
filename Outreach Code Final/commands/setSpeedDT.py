import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class setSpeedDT(TimedCommand):

    def __init__(self, timeout = 0):
        super().__init__('setSpeedDT', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.Joystick0 = self.getRobot().joystick0
        self.Joystick1 = self.getRobot().joystick1

        self.maxspeed = 0.90

    def execute(self):
        left = self.Joystick0.getY()
        right = self.Joystick1.getY()
        self.DT.tankDrive(-left * self.maxspeed ,-right * self.maxspeed)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
