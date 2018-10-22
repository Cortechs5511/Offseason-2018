import wpilib
import networktables
from networktables import NetworkTables

table = NetworkTables.getTable("limelight")
tx = table.getNumber("tx", None)
ty = table.getNumber("ty", None)
ta = table.getNumber("ta", None)
ts = table.getNumber("ts", None)

SmartDashboard.putNumber("tx", tx)
SmartDashboard.putNumber("ty", ty)
SmartDashboard.putNumber("ta", ta)
SmartDashboard.putNumber("ts", ts)
