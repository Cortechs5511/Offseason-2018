import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setFixedLift(Command):

    def __init__(self, speed=0):
        super().__init__('setFixedLift')
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift
        self.speed = speed

        SmartDashboard.putData("setFixedLift", self)

    def execute(self):
        self.Lift.setSpeed(self.speed)

    def interrupted(self):
        self.Lift.setSpeed(0)

    def end(self):
        self.Lift.setSpeed(0)
