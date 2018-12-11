import math
import wpilib

from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class driveVision(TimedCommand):

    def __init__(self, timeout = 300, PController = .03):
        super().__init__('TurnVisionPID', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.limelight = self.getRobot().limelight

        self.PController = PController

        self.dist_tol = 10

    def initialize(self):
        #self.DT.setAngle(self.Limelight.Gettx())
        distance = self.limelight.getDistance()
        angle = self.Drive.getAngle() + self.limelight.getTx()

        self.distance = distance + self.DT.getAvgDistance()
        self.DT.setCombined(distance=distance, angle=angle)

    def execute(self):
        #self.DT.setAngle(self.Limelight.Gettx())
        '''power = self.PController * self.Limelight.Gettx()
        self.DT.tankDrive(power,-1*power)'''
        self.DT.tankDrive()

    def isFinished(self):
        #return (abs(self.Limelight.Gettx())<2 and self.DT.getAvgAbsVelocity()<0.05) or self.isTimedOut()
        return (abs(self.limelight.getDistance())<self.dist_tol and self.DT.getAvgAbsVelocity()<0.05) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
