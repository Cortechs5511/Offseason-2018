import math

import wpilib
from wpilib.command import Command

class setFixedIntake(Command):

    def __init__(self, speed = 0, maxtime = 300):
        super().__init__('SetFixedIntake')
        self.requires(self.getRobot().intake)
        self.Intake = self.getRobot().intake
        self.speed = speed

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def execute(self):
        self.Intake.setSpeed(self.speed)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.Intake.setSpeed(0)

    def end(self):
        self.Intake.setSpeed(0)
