import math

import wpilib
from wpilib.command import Command
from wpilib.command import InstantCommand

class Zero(InstantCommand):

    def __init__(self):
        super().__init__('Zero')
        self.requires(self.getRobot().wrist)
        self.requires(self.getRobot().lift)
        self.Wrist = self.getRobot().wrist
        self.Lift = self.getRobot().lift

    def initialize(self):
        self.Wrist.zero()
        self.Lift.zero()

    def interrupted(self):
        self.Wrist.setSpeed(0)

    def end(self):
        self.Wrist.setSpeed(0)
