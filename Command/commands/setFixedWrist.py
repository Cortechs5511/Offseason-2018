import math

import wpilib
from wpilib.command import Command

class setFixedWrist(Command):

    def __init__(self, speed = 0, maxtime = 300):
        super().__init__('setFixedWrist')
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist
        self.speed = speed

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def execute(self):
        self.Wrist.setSpeed(self.speed)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.Wrist.setSpeed(0)

    def end(self):
        self.Wrist.setSpeed(0)
