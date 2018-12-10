import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from path import PathFinder
from path import Ramsetes

class DrivePath(TimedCommand):

    def __init__(self, name="DriveStraight", follower="PathFinder", timeout = 10):
        super().__init__('DrivePath', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.name = name
        self.follower = follower

        self.Ramsetes = self.DT.Ramsetes
        self.PathFinder = self.DT.PathFinder

    def initialize(self):
        self.DT.setPath(name=self.name, follower=self.follower)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        if(self.follower=="PathFinder"): return (self.PathFinder.isFinished()  or self.isTimedOut())
        elif(self.follower=="Ramsetes"): return (self.Ramsetes.isFinished()  or self.isTimedOut())
        else: return True

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
        if(self.follower=="PathFinder"): self.PathFinder.disablePID()
        elif(self.follower=="Ramsetes"): self.Ramsetes.disablePID()
