import wpilib.buttons
from wpilib.drive import DifferentialDrive
import ctre

class MyRobot(wpilib.IterativeRobot):

    def __init__(self):
        super().__init__()

    def robotInit(self):
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

        #Two options for initializing drive sides, test both
        self.left = self.DriveLeft1
        self.right = wpilib.SpeedControllerGroup(self.DriveRight1)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        self.LeftJoystick = wpilib.Joystick(0)
        self.RightJoystick = wpilib.Joystick(1)

    def teleopInit(self):
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
        self.myRobot.tankDrive((self.LeftJoystick.getY()) * -1 * self.Max_Speed, (self.RightJoystick.getY()) * -1 * self.Max_Speed)

if __name__ == '__main__':
    wpilib.run(MyRobot)
