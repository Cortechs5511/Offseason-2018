import math
import wpilib
from wpilib.command import Command
from sensors.DTEncoders import DTEncoders
#from sensors.navx import NavX

class DriveStraightDistancePID(Command):

    def __init__(self, distance = 10):
        super().__init__('DriveStraightDistancePID')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.setpoint = distance
        self.DT.encoders.enablePID()
#        self.DT.navx.enablePID()

        self.TolDist = 0.5 #feet

    def execute(self):
        dist = self.DT.getAvgDistance()

        self.distError = self.setpoint-dist
        speed = -(self.distError)/(self.setpoint+1) * 0.5 + 0.4

        ePID = self.DT.encoders.getPID()
#        nPID = self.DT.navx.getPID()
        nPID = ePID
        err = (ePID+nPID)/2.0

        LeftSpeed = speed + err
        RightSpeed = speed - err

        self.DT.tankDrive(LeftSpeed,RightSpeed)

        if abs(self.distError) < self.TolDist and (LeftSpeed+RightSpeed) / 2 < 0.2:  self.done = True
        else: self.done = False

    def interrupted(self):
        self.DT.encoders.disablePID()
#        self.DT.navx.disablePID()
        self.DT.tankDrive(0,0)

    def isFinished(self):
        return self.done


    def end(self):
        self.DT.encoders.disablePID()
#        self.DT.navx.disablePID()
        self.DT.tankDrive(0,0)
