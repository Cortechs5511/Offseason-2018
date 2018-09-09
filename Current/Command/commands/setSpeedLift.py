from networktables import NetworkTables
from wpilib.command import Command
import math

class setSpeedLift(Command):

    def __init__(self):
        super().__init__('SetLiftSpeed')
        self.requires(self.getRobot().lift)
        self.Lift = self.getRobot().lift

    def execute(self):
        liftPos = self.Lift.getHeight()
        liftSpeed = self.getRobot().xbox.getY(0)
        if liftSpeed > 0.1 and lift_pos < 48: self.Lift.setSpeed(liftSpeed)
        elif liftSpeed < - 0.1 and lift_pos > 20: self.Lift.setSpeed(liftSpeed)
        else: self.Lift.setSpeed(0)

    def interrupted(self):
        self.Lift.setSpeed(0)

    def end(self):
        self.Lift.setSpeed(0)
