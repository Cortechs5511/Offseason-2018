import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from CRLibrary.path import PathFinder
from CRLibrary.path import Ramsetes

class DrivePath(TimedCommand):

    def __init__(self, name="DriveStraight", follower="PathFinder", timeout = 10):
        super().__init__('DrivePath', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.name = name
        self.follower = follower

        self.Path = self.DT.Path

    def initialize(self):
        self.DT.setPath(name=self.name, follower=self.follower)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return self.Path.isFinished() or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
        self.Path.disablePID()
