import math
import wpilib
from wpilib.command import Command
from sensors.DTEncoders import DTEncoders
from sensors.navx import NavX

class DriveStraightDistance(Command):

    def __init__(self, distance = 0):
        super().__init__('DriveStraightDistance')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.setpoint = distance

    def execute(self):
        Kp_Dist = 0.2
        Kp_Angle = 0.2
        Tol_Angle = 3
        self.Tol_Dist = 10
        self.AverageDistance = ( DTEncoders.getDistance()[0] + DTEncoders.getDistance()[1] ) / 2
        self.error = math.abs(self.setpoint) - self.AverageDistance
        CurrAngle = NavX.getAngle()
        AngleError = CurrAngle
        # get speed based on how far you travelled
        if math.fabs(AverageDistance) < math.fabs(self.setpoint):
            speed = Kp_Dist * error
        else:
            speed = 0

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
        if self.error < self.Tol_Dist:
            return True
        else:
            return False

    def end(self):
        self.DT.tankDrive(0,0)
