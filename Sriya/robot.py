import wpilib
import wpilib.buttons
from wpilib.drive import DifferentialDrive
import ctre

class MyRobot(wpilib.IterativeRobot):



    def __init__(self):
        super().__init__()
        #self.turn_power = 0
        self.Max_Speed = 0.85

    def robotInit(self):
        '''Robot initialization function'''

        # object that handles basic drive operations
        self.DriveLeft1 = ctre.WPI_TalonSRX(10)
        self.DriveRight1 = ctre.WPI_TalonSRX(20)
        self.DriveLeft2 = ctre.WPI_VictorSPX(11)
        self.DriveLeft3 = ctre.WPI_VictorSPX(12)
        self.DriveRight2 = ctre.WPI_VictorSPX(21)
        self.DriveRight3 = ctre.WPI_VictorSPX(22)
        self.LeftEncoder = wpilib.Encoder(0,1)
        self.RightEncoder = wpilib.Encoder(2,3)

        self.left = wpilib.SpeedControllerGroup(self.DriveLeft1, self.DriveLeft2, self.DriveLeft3)
        self.right = wpilib.SpeedControllerGroup(self.DriveRight1, self.DriveRight2, self.DriveRight3)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        # joysticks 1 & 2 on the driver station
        self.LeftJoystick = wpilib.Joystick(0)
        self.RightJoystick = wpilib.Joystick(1)

    #def __init__(self, kp=1):
        #super().__init__()
        #self.turn_power = kp * (self.RightEncoder - self.LeftEncoder)

    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''
        self.myRobot.tankDrive((self.LeftJoystick.getY()) * -1 * self.Max_Speed , (self.RightJoystick.getY()) * -1 * self.Max_Speed )

if __name__ == '__main__':
    wpilib.run(MyRobot)