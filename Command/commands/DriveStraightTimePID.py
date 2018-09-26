import math
import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand
from sensors.DTEncoders import DTEncoders
from sensors.navx import NavX

class DriveStraightTimePID(TimedCommand):

    def __init__(self,speed = 0, timeout = 0):
        super().__init__('DriveStraightTimePID', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.speed = speed

        self.DT.encoders.enablePID()
        self.DT.navx.enablePID()

    def execute(self):
        ePID = self.DT.encoders.getPID()
        nPID = self.DT.navx.getPID()
        err = (ePID+nPID)/2.0

        LeftSpeed = self.speed + err
        RightSpeed = self.speed - err
        self.DT.tankDrive(LeftSpeed,RightSpeed)

    def interrupted(self):
        self.DT.encoders.disablePID()
        self.DT.navx.disablePID()
        self.DT.tankDrive(0,0)

    def isFinished(self):
         return self.isTimedOut()

    def end(self):
        self.DT.encoders.disablePID()
        self.DT.navx.disablePID()
        self.DT.tankDrive(0,0)
