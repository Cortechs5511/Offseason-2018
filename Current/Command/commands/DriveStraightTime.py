import math
import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand
from sensors.DTEncoders import DTEncoders
from sensors.navx import NavX

class DriveStraightTime(TimedCommand):

    def __init__(self,speed = 0):
        super().__init__('DriveStraightTime', timeoutInSeconds = 0)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.speed = speed

    def execute(self):
        Kp_Angle = 0.2
        Tol_Angle = 3
        CurrAngle = NavX.getAngle()
        AngleError = CurrAngle
        # get speed based on how far you travelled

        if CurrAngle < Tol_Angle * -1:
            LeftSpeed = speed - (CurrAngle * Kp_Angle)
            RightSpeed = speed
        if CurrAngle > Tol_Angle:
            RightSpeed = (speed + (CurrAngle * Kp_Angle)) * math.copysign(1,self.setpoint)
            LeftSpeed = speed
        else:
            LeftSpeed = speed
            RightSpeed = speed

        self.DT.tankDrive(LeftSpeed,RightSpeed)

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def isFinished(self):
         return self.isTimedOut()

    def end(self):
        self.DT.tankDrive(0,0)
