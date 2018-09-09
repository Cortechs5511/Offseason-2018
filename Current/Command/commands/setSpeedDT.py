from networktables import NetworkTables
from wpilib.command import Command
import math

class setSpeedDT(Command):

    def __init__(self):
        super().__init__('setSpeedDT')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

    def execute(self):
        left = self.getRobot().joystick0.getY()
        right = self.getRobot().joystick1.getY()
        self.DT.tankDrive(left,right)

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def end(self):
        self.DT.tankDrive(0,0)
