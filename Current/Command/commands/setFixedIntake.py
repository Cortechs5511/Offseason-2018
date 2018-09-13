import math

import wpilib
from wpilib.command import Command
from wpilib import SmartDashboard

class setFixedIntake(Command):

    def __init__(self, speed = 0):
        super().__init__('SetFixedIntake')
        self.requires(self.getRobot().intake)
        self.Intake = self.getRobot().intake
        self.speed = speed

        SmartDashboard.putData("setFixedLift", self)

    def execute(self):
        self.Intake.setSpeed(self.speed)

    def interrupted(self):
        self.Intake.setSpeed(0)

    def end(self):
        self.Intake.setSpeed(0)
