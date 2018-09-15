import math
import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand
from sensors.DTEncoders import DTEncoders
from sensors.navx import NavX

class DriveStraightTime(TimedCommand):

    def __init__(self,speed = 0, timeout = 0):
        super().__init__('DriveStraightTime', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.speed = speed

        self.kpAngle = 0.05
        self.TolAngle = 10 #degrees

    def execute(self):
        angle = self.DT.getAngle()
        self.angleError = angle #-0

        LeftSpeed = self.speed
        RightSpeed = self.speed
        if abs(self.angleError) > self.TolAngle:
            LeftSpeed = self.speed - (self.angleError * self.kpAngle)
            RightSpeed = self.speed + (self.angleError * self.kpAngle)

        self.DT.tankDrive(LeftSpeed,RightSpeed)

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def isFinished(self):
         return self.isTimedOut()

    def end(self):
        self.DT.tankDrive(0,0)
