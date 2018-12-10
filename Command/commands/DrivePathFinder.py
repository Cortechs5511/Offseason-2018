import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from path import PathFinder

class DrivePathFinder(TimedCommand):

    def __init__(self, name="DriveStraight", timeout = 10):
        super().__init__('DrivePathFinder', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.name = name

    def initialize(self):
        self.DT.setPathFinder(name=self.name)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return (PathFinder.isFinished()  or self.isTimedOut())

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
