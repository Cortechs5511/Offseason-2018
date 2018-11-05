import math

import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand

class setFixedIntake(TimedCommand):

    def __init__(self, speed = 0, timeout = 0):
        super().__init__('SetFixedIntake', timeoutInSeconds = timeout)
        self.requires(self.getRobot().intake)
        self.Intake = self.getRobot().intake
        self.speed = speed

    def execute(self):
        self.Intake.setSpeed(self.speed)

    def isFinished(self):
        return self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.Intake.setSpeed(0)
