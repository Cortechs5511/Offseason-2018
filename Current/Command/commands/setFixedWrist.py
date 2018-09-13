import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setFixedWrist(Command):

    def __init__(self, speed=0):
        super().__init__('setFixedWrist')
        self.requires(self.getRobot().wrist)
        self.Wrist = self.getRobot().wrist
        self.speed = speed

        SmartDashboard.putData("setFixedWrist", self)

    def execute(self):
        self.Wrist.setSpeed(self.speed)

    def interrupted(self):
        self.Wrist.setSpeed(0)

    def end(self):
        self.Wrist.setSpeed(0)
