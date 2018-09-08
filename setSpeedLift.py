from wpilib.command import Command
import math
from networktables import NetworkTables

class setLiftSpeed(Command):

    def __init__(self):
        super().__init__('Follow Joystick')
        self.smartDashboard = NetworkTables.getTable("SmartDashboard")

        self.requires(self.getRobot().lift)


    def execute(self):
        Lift = self.getRobot().lift
        lift_pos = Lift.getHeight()
        gravity_lift = self.getLiftGravity()
        Joystick2 = self.getRobot().xbox

        liftSpeed = Joystick2.getY(0)

        # set speed according to gravity value
        if liftSpeed > 0.1 and lift_pos < 48:
            Lift.setSpeed(liftSpeed + gravity_lift)
        elif liftSpeed < - 0.1 and lift_pos > 20:
            Lift.setSpeed(liftSpeed + gravity_lift)
        else:
            Lift.setSpeed(gravity_lift)
