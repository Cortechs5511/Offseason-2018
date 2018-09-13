from networktables import NetworkTables
from wpilib.command import Command
import math

class setFixedLift(Command):

    def __init__(self, speed=0):
        super().__init__('setFixedLift')
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift
        self.speed = speed

    def execute(self):
        self.Lift.setSpeed(self.speed)

    def interrupted(self):
        self.Lift.setSpeed(0)

    def end(self):
        self.Lift.setSpeed(0)
