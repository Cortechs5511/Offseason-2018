import math

import wpilib
from wpilib.command import Command

class setFixedLift(Command):

    def __init__(self, speed = 0, maxtime = 300):
        super().__init__('setFixedLift')
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift
        self.speed = speed

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def execute(self):
        self.Lift.setSpeed(self.speed)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.Lift.setSpeed(0)

    def end(self):
        self.Lift.setSpeed(0)
