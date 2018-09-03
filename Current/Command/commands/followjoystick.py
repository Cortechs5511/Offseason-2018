from wpilib.command import Command
from wpilib.drive import DifferentialDrive
import math
from networktables import NetworkTables

class FollowJoystick(Command):

    def __init__(self):
        super().__init__('Follow Joystick')
        self.smartDashboard = NetworkTables.getTable("SmartDashboard")

        self.requires(self.getRobot().lift)
        self.requires(self.getRobot().wrist)
        self.requires(self.getRobot().intake)
        self.requires(self.getRobot().drive)


    def execute(self):
        Lift = self.getRobot().lift
        Wrist = self.getRobot().wrist
        Intake = self.getRobot().intake
        Joystick = self.getRobot().joystick
        Joystick1 = self.getRobot().joystick1
        wrist_pos = Wrist.getDataUnits()[0]
        lift_pos = Lift.getDataUnits()[0]
        gravity_lift = 0.3
        gravity_wrist = 0.3
        wrist_tol = 45 #degree position at which wrist needs power to be held up
        lift_tol = 10 #Inches above the robot at which lift needs to be held up
        self.smartDashboard.putNumber("Position", wrist_pos)

        # determine gravity value for lift
        if lift_pos > lift_tol:
            y = gravity_lift * -1
        elif lift_pos < lift_tol:
            y = gravity_lift
        else:
            y = 0

        # set speed according to gravity value
        if Joystick.getZ() > 0.1:
            Lift.setSpeed(Joystick.getZ() + y)
        elif Joystick.getZ() * -1 <- 0.1:
            Lift.setSpeed(Joystick.getZ() - y)
        else:
            Lift.setSpeed(y)

        #DRIVE
        left = Joystick.getY()
        right = Joystick1.getY()
        self.getRobot().drive.tankDrive(left,right)

        # determine gravity value for wrist
        if wrist_pos > wrist_tol:
            x = gravity_wrist * -1
        elif wrist_pos * -1 < wrist_tol:
            x = gravity_wrist
        else:
            x = 0

        # set speed according to gravity value
        if Joystick.getRawButton(1) == True:
            Wrist.setSpeed(-0.4 - x)
        elif Joystick.getRawButton(2) == True:
            Wrist.setSpeed(0.4 + x)
        else:
            self.getRobot().wrist.setSpeed(x)

        # INTAKE
        if Joystick.getRawButton(3) == True:
            Intake.setSpeed(0.7)
        elif Joystick.getRawButton(4) == True:
            Intake.setSpeed(-0.7)
        else:
            Intake.setSpeed(0)
