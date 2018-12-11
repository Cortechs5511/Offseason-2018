import wpilib.buttons
from wpilib.command.subsystem import Subsystem

from wpilib import SmartDashboard
from networktables import NetworkTables

from commands.getLimelightData import getLimelightData

class Limelight(Subsystem):

    def __init__(self, Robot):
        self.table = NetworkTables.getTable("limelight")
        self.table.putNumber('ledMode',1)

        self.tv = 0
        self.tx = 0
        self.ty = 0
        self.ta = 0
        self.ts = 0
        self.tl = 0

    def readLimelightData(self):
        self.tv = self.table.getNumber('tv',None)
        self.tx = self.table.getNumber('tx',None)
        self.ty = self.table.getNumber('ty',None)
        self.ta = self.table.getNumber('ta',None)
        self.ts = self.table.getNumber('ts',None)
        self.tl = self.table.getNumber('tl',None)

    def get(self):
        return [self.tv, self.tx, self.ty, self.ta, self.ts, self.tl]

    def initDefaultCommand(self):
        self.setDefaultCommand(getLimelightData())

    def UpdateDashboard(self):
        SmartDashboard.putNumber("Limelight_tv", self.tv)
        SmartDashboard.putNumber("Limelight_tv", self.tx)
        SmartDashboard.putNumber("Limelight_tv", self.ty)
        SmartDashboard.putNumber("Limelight_tv", self.ta)
        SmartDashboard.putNumber("Limelight_tv", self.ts)
        SmartDashboard.putNumber("Limelight_tv", self.tl)
