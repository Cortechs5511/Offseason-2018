import math

import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand

class setFixedWrist(TimedCommand):

    def __init__(self, speed = 0, timeout = 0):
        super().__init__('setFixedWrist', timeoutInSeconds = timeout)
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist
        self.speed = speed

    def execute(self):
        self.Wrist.setSpeed(self.speed)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.Wrist.setSpeed(0)
