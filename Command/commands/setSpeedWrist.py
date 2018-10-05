import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from wpilib import SmartDashboard

class setSpeedWrist(TimedCommand):

    def __init__(self, timeout = 0):
        super().__init__('setSpeedWrist', timeoutInSeconds = timeout)
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist

    def execute(self):
        wristPos = self.Wrist.getAngle()
        Joystick = self.getRobot().xbox
        self.Wrist.setSpeed(0.4* Joystick.getX(1))

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.Wrist.end()

    def end(self):
        self.Wrist.setSpeed(0)
