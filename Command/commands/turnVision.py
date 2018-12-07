import math
import wpilib

from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class TurnVision(TimedCommand):

    def __init__(self, timeout = 0):
        super().__init__('TurnVisionPID', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.Limelight = self.getRobot().limelight

    def initialize(self):
        self.DT.setAngle(self.Limelight.Gettx())

    def execute(self):
        self.DT.setAngle(self.Limelight.Gettx())
        self.DT.tankDrive()

    def isFinished(self):
        return (abs(self.Limelight.Gettx())<2 and self.DT.getAvgAbsVelocity()<0.05) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
