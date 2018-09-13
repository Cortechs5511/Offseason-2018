from networktables import NetworkTables
from wpilib.command import Command
import math

class setFixedDT(Command):

    def __init__(self, leftSpeed=0, rightSpeed=0):
        super().__init__('setFixedDT')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.lspeed = leftSpeed
        self.rspeed = rightSpeed

    def execute(self):
        self.DT.tankDrive(self.leftSpeed,self.rightSpeed)

    def interrupted(self):
        self.DT.tankDrive(0,0)

    def end(self):
        self.DT.tankDrive(0,0)
