from networktables import NetworkTables
from wpilib.command import Command
import math

class setFixedIntake(Command):

    def __init__(self, speed = 0):
        super().__init__('SetFixedIntake')
        self.requires(self.getRobot().intake)
        self.Intake = self.getRobot().intake
        self.speed = speed

    def execute(self):
        self.Intake.setSpeed(self.speed)

    def interrupted(self):
        self.Intake.setSpeed(0)

    def end(self):
        self.Intake.setSpeed(0)
