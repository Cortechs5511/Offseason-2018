import math
import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard
from sensors.DTEncoders import DTEncoders
#from sensors.navx import NavX

class DriveStraightDistancePID(Command):

    def __init__(self, distance = 10, Debug = False, maxtime=300):
        super().__init__('DriveStraightDistancePID')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.maxtime = maxtime
        self.timer = self.getRobot().timer
        self.setpoint = distance
        self.finished = False

    def initialize(self):
        setpoint = self.setpoint + self.DT.pidGet()
        self.DT.setDistance(setpoint)

    def isFinished(self):
        rate = abs(self.DT.encoders.getAvgVelocity())
        minrate = 0.25

        if self.DT.distController.onTarget() and rate < minrate or self.timer.get() > self.maxtime: return True
        else: return False

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
