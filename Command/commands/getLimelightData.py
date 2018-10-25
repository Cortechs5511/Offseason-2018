import wpilib
import networktables
from wpilib.command import Command
from networktables import NetworkTables

class getLimelightData(Command):

    def __init__(self, timeout = 0):
        super().__init__('getLimelightData')
        self.table = NetworkTables.getTable("limelight")
        self.llheight = 5 #height of limelight off the floor

    def execute(self):
        self.tx = self.table.getNumber("tx", None)
        self.ty = self.table.getNumber("ty", None)
        self.ta = self.table.getNumber("ta", None)
        self.ts = self.table.getNumber("ts", None)

    def getDistance(self):
        d = (5.5 - self.llheight) / tan(self.ty)
