import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard


class setFixedWrist(TimedCommand):

    def __init__(self, speed = 0, timeout = 0):
        super().__init__('setFixedWrist', timeoutInSeconds = timeout)
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist
        self.speed = speed

    def execute(self):
        #self.Wrist.setSpeed(self.speed)
        pass

    def interrupted(self):
        self.end()

    def end(self):
        self.Wrist.setSpeed(0)
