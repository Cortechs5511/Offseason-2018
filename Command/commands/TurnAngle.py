import math
import wpilib
from wpilib.command import Command
from sensors.DTEncoders import DTEncoders
from sensors.navx import NavX

class TurnAngle(Command):

    def __init__(self, angle = 0):
        super().__init__('TurnAngle')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.setpoint = angle
        self.speed = 0.3

        self.KpAngle = 0.005
        self.TolAngle = 3

    def execute(self):
        angle = self.DT.navx.getAngle()
        self.AngleError = self.setpoint - angle
        LeftSpeed = self.speed + (self.KpAngle * self.AngleError)
        RightSpeed = self.speed - (self.KpAngle * self.AngleError)
        self.DT.tankDrive(LeftSpeed,RightSpeed)

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def isFinished(self):
        if abs(self.AngleError) <= self.TolAngle: return True
        else: return False

    def end(self):
        self.DT.tankDrive(0,0)
