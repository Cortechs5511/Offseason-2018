import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setPositionLift(Command):

    def __init__(self, setpoint = 0, Debug = False, maxtime = 300):
        super().__init__('setPositionLift')
        self.setpoint = setpoint
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift
        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def initialize(self):
        self.Lift.setHeight(self.setpoint)

    def isFinished(self):
        return self.timer.get() > self.maxtime

    def end(self):
        self.Lift.setSpeed(0)

    def interrupted(self):
        self.end()
