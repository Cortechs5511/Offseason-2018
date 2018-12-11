import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.path import odometry as od
from CRLibrary.path import PathFinder
from CRLibrary.path import Ramsetes

class Path():

    def __init__(self, DT, model, odometer, getDistances, follower="PathFinder"):

        self.PathFinder = PathFinder.PathFinder(DT, model, odometer, getDistances)
        self.Ramsetes = Ramsetes.Ramsetes(DT, model, odometer)
        self.setFollower(follower)

    def setFollower(self, follower):
        self.follower = follower

    def enablePID(self):
        if(self.follower=="PathFinder"): self.PathFinder.enablePID()
        elif(self.follower=="Ramsetes"): self.Ramsetes.enablePID()

    def disablePID(self):
        if(self.follower=="PathFinder"): self.PathFinder.disablePID()
        elif(self.follower=="Ramsetes"): self.Ramsetes.disablePID()

    def initPath(self, name):
        if(self.follower=="PathFinder"): self.PathFinder.initPath(name)
        elif(self.follower=="Ramsetes"): self.Ramsetes.initPath(name)

    def followPath(self):
        if(self.follower=="PathFinder"): return self.PathFinder.followPath()
        elif(self.follower=="Ramsetes"): return self.Ramsetes.followPath()

    def isFinished(self):
        if(self.follower=="PathFinder"): self.PathFinder.isFinished()
        elif(self.follower=="Ramsetes"): self.Ramsetes.isFinished()
