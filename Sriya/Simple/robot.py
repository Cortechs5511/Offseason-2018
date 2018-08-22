import wpilib
import wpilib.buttons
from wpilib.drive import DifferentialDrive
import ctre


class MyRobot(wpilib.IterativeRobot):

    def __init__(self):
        super().__init__()
        # self.turn_power = 0
        self.Max_Speed = 0.85

    def robotInit(self):
        '''Robot initialization function'''

        # object that handles basic drive operations
        self.DriveLeft1 = ctre.WPI_TalonSRX(10)
        self.DriveLeft2 = ctre.WPI_VictorSPX(11)
        self.DriveLeft3 = ctre.WPI_VictorSPX(12)
        self.DriveLeft2.set(ctre.WPI_VictorSPX.ControlMode.Follower, 10)
        self.DriveLeft3.set(ctre.WPI_VictorSPX.ControlMode.Follower, 10)

        self.DriveRight1 = ctre.WPI_TalonSRX(20)
        self.DriveRight2 = ctre.WPI_VictorSPX(21)
        self.DriveRight3 = ctre.WPI_VictorSPX(22)
        self.DriveRight2.set(ctre.WPI_VictorSPX.ControlMode.Follower, 20)
        self.DriveRight3.set(ctre.WPI_VictorSPX.ControlMode.Follower, 20)

        self.LeftEncoder = wpilib.Encoder(0, 1)
        self.RightEncoder = wpilib.Encoder(2, 3)

        self.left = wpilib.SpeedControllerGroup(self.DriveLeft1)
        self.right = wpilib.SpeedControllerGroup(self.DriveRight1)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        # intake
        self.Lintake = ctre.WPI_TalonSRX(50)
        self.Rintake = ctre.WPI_TalonSRX(51)
        self.Rintake.set(ctre.WPI_TalonSRX.ControlMode.Follower, 50)

        # lift
        self.Lift1 = ctre.WPI_TalonSRX(30)
        self.Lift2 = ctre.WPI_TalonSRX(31)
        self.Lift2.set(ctre.WPI_TalonSRX.ControlMode.Follower, 30)

        # wrist
        self.wrist = ctre.WPI_TalonSRX(40)

        # joysticks 1 & 2 on the driver station
        self.LeftJoystick = wpilib.Joystick(0)
        self.RightJoystick = wpilib.Joystick(1)
        self.cntrlr = wpilib.XboxController(2)

    # def __init__(self, kp=1):
    # super().__init__()
    # self.turn_power = kp * (self.RightEncoder - self.LeftEncoder)

    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''
        self.myRobot.tankDrive((self.LeftJoystick.getY()) * -1 * self.Max_Speed,
                               (self.RightJoystick.getY()) * -1 * self.Max_Speed)

        if self.cntrlr.getYButton() == True:
            self.Lift1.set(-0.7)
        elif self.cntrlr.getAButton() == True:
            self.Lift1.set(0.7)
        else:
            self.Lift1.set(0)

        if self.cntrlr.getXButton() == True:
            self.wrist.set(-0.3)
        elif self.cntrlr.getBButton() == True:
            self.wrist.set(0.3)
        else:
            self.wrist.set(0)

        if self.cntrlr.getTriggerAxis(0) > 0.05:
            self.Lintake.set(0.7)
        elif self.cntrlr.getTriggerAxis(1) > 0.05:
            self.Lintake.set(-0.7)
        else:
            self.Lintake.set(0)


if __name__ == '__main__':
    wpilib.run(MyRobot)
