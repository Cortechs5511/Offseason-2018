import math
import wpilib

from wpilib import SmartDashboard
from wpilib.command import Command


class TurnAnglePID(Command):

    def __init__(self, angle = 0, DEBUG=False, maxtime=300):
        super().__init__('TurnAnglePID')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.maxtime = maxtime
        self.timer = self.getRobot().timer

        self.angle = angle

    def initialize(self):
        self.DT.setAngle(self.angle)

    def isFinished(self):
        rate = abs(self.DT.getAvgAbsVelocity())
        minrate = 0.25

        if self.DT.distController.onTarget() and rate < minrate or self.timer.get() > self.maxtime: return True
        else: return False

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
