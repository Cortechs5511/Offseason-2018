import wpilib
import networktables
from wpilib.command import TimedCommand
from networktables import NetworkTables

class getLimelightData(TimedCommand):

    def __init__(self, timeout = 0):
        super().__init__('getLimelightData', timeoutInSeconds=timout)

        self.requires(self.getRobot().limelight)
        self.LL = self.getRobot().limelight

    def execute(self):
        self.LL.readLimelightData()
