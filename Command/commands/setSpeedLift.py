import math

import wpilib
from wpilib.command import Command

class setSpeedLift(Command):

    def __init__(self, maxtime = 300):
        super().__init__('setSpeedLift')
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def execute(self):
        liftPos = self.Lift.getHeight()
        liftSpeed = self.getRobot().xbox.getY(0)
        if liftSpeed > 0.1 and liftPos < 28: self.Lift.setSpeed(liftSpeed)
        elif liftSpeed < - 0.1 and liftPos > -1: self.Lift.setSpeed(liftSpeed)
        else: self.Lift.setSpeed(0)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def interrupted(self):
        self.Lift.setSpeed(0)

    def end(self):
        self.Lift.setSpeed(0)
