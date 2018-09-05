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
        self.smartDashboard.putNumber("lift_gravity", self.getLiftGravity())


    def getLiftGravity(self):
        return self.smartDashboard.getNumber("lift_gravity", 0.0)

    def getWristGravity(self):
        return self.smartDashboard.getNumber("wrist_gravity", 0.0)

    def execute(self):
        Lift = self.getRobot().lift
        Wrist = self.getRobot().wrist
        Intake = self.getRobot().intake
        Joystick = self.getRobot().joystick
        Joystick1 = self.getRobot().joystick1
        Joystick2 = self.getRobot().xbox
        wrist_pos = Wrist.getDataUnits()[0]
        lift_pos = Lift.getDataUnits()[0]
        gravity_lift = self.getLiftGravity()
        gravity_wrist = self.getLiftGravity()
        wrist_tol = 45 #degree position at which wrist needs power to be held up
        lift_tol = 10 #Inches above the robot at which lift needs to be held up
        self.smartDashboard.putNumber("Position", wrist_pos)

        # determine gravity value for lift
        '''if lift_pos > lift_tol:
            y = gravity_lift * -1
        elif lift_pos < lift_tol:
            y = gravity_lift
        else:
            y = 0'''

        lift_height = lift_pos / 2380
        y = lift_height * gravity_lift / 50
        self.smartDashboard.putNumber("lift_height",lift_height)

        y = -1 * gravity_lift

        # set speed according to gravity value
        if Joystick2.getY(0) > 0.1:
            Lift.setSpeed(Joystick2.getY(0) + y)
        elif Joystick2.getY(0) < - 0.1:
            Lift.setSpeed(Joystick2.getY(0) - y)
            self.smartDashboard.putNumber("LiftWork?",Joystick.getZ())
        else:
            Lift.setSpeed(y)


        #DRIVE
        left = Joystick.getY()
        right = Joystick1.getY()
        self.getRobot().drive.tankDrive(left,right)

        # determine gravity value for wrist
        self.smartDashboard.putNumber("wrist_gravity",gravity_wrist)
        '''if wrist_pos > wrist_tol:
            x = gravity_wrist * -1
        elif wrist_pos * -1 < wrist_tol:
            x = gravity_wrist
        else:
            x = 0'''

        wrist_angle = wrist_pos / 2222
        x = wrist_angle * gravity_wrist / 90
        self.smartDashboard.putNumber("wrist_angle",wrist_angle)

        # set speed according to gravity value
        if Joystick2.getXButton() == True:
            Wrist.setSpeed(-0.4 - x)
        elif Joystick2.getBButton() == True:
            Wrist.setSpeed(0.4 + x)
        else:
            self.getRobot().wrist.setSpeed(x)

        # INTAKE
        if Joystick2.getTriggerAxis(0) == True:
            Intake.setSpeed(0.7)
        elif Joystick2.getTriggerAxis(1) == True:
            Intake.setSpeed(-0.7)
        else:
            Intake.setSpeed(0)
