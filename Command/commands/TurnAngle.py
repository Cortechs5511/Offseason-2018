import math
import wpilib
from wpilib.command import Command
from sensors.DTEncoders import DTEncoders
from sensors.navx import NavX

class TurnAngle(Command):

    def __init__(self, angle = 0, speed = 0):
        super().__init__('TurnAngle')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.setpoint = angle
        self.speed = speed

    def execute(self):
        Kp_Angle = 0.2
        Tol_Angle = 3
        CurrAngle = NavX.getAngle()
        AngleError = math.fabs(self.setpoint) - CurrAngle
        # get speed based on how far you travelled

        if math.fabs(AngleError) > Tol_Angle:
            LeftSpeed = self.speed + (CurrAngle * Kp_Angle * math.copysign(1,self.setpoint))
            RightSpeed = self.speed - (currAngle * Kp_Angle * math.copysign(1,self.setpoint))
        else:
            pass


        self.DT.tankDrive(LeftSpeed,RightSpeed)

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def isFinished(self):
        if math.fabs(AngleError) <= Tol_Angle:
            return True
        else:
            return False

    def end(self):
        self.DT.tankDrive(0,0)
