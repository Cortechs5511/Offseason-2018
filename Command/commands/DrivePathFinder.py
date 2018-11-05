import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from wpilib import SmartDashboard

class DrivePathFinder(TimedCommand):

    def __init__(self, name=None, timeout = 0):
        super().__init__('DrivePathFinder', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.name = name

    def initialize(self):
        self.DT.setPathFinder(name=self.name)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return self.DT.spline[0].isFinished() or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
