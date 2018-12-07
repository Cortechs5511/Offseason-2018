import math
import wpilib

from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class TurnVision(TimedCommand):

    def __init__(self, timeout = 300, PController = .03):
        super().__init__('TurnVisionPID', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.Limelight = self.getRobot().limelight
        self.PController = PController

    def initialize(self):
        #self.DT.setAngle(self.Limelight.Gettx())
        pass

    def execute(self):
        #self.DT.setAngle(self.Limelight.Gettx())
        power = self.PController * self.Limelight.Gettx()
        self.DT.tankDrive(power,-1*power)

    def isFinished(self):
        #return (abs(self.Limelight.Gettx())<2 and self.DT.getAvgAbsVelocity()<0.05) or self.isTimedOut()
        return False

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
