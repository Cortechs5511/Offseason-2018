import math
import wpilib
from wpilib.command import Command
from sensors.DTEncoders import DTEncoders
#from sensors.navx import NavX

class DriveStraightDistance(Command):

    def __init__(self, distance = 0):
        super().__init__('DriveStraightDistance')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.setpoint = distance

        self.kpDist = 0.2
        self.kpAngle = 0.05
        self.TolDist = 0.5 #feet
        self.TolAngle = 10 #degrees


    def execute(self):
        dist = self.DT.getAvgDistance()
        angle = self.DT.getAngle()

        self.distError = self.setpoint - dist
        self.angleError = angle #-0

        # get speed based on how far you travelled
        speed = 0
        if abs(dist-self.setpoint)>self.TolDist: speed = self.kpDist * self.distError


        LeftSpeed = speed
        RightSpeed = speed
        if abs(self.angleError) > self.TolAngle:
            LeftSpeed = speed - (self.angleError * self.kpAngle)
            RightSpeed = speed + (self.angleError * self.kpAngle)

        self.DT.tankDrive(LeftSpeed,RightSpeed)

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def isFinished(self):
        if abs(self.distError) < self.TolDist and abs(self.angleError) < self.TolAngle: return True
        return False

    def end(self):
        self.DT.tankDrive(0,0)
