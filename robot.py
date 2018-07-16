import wpilib
import wpilib.drive
import ctre

#I, Ashish, wrote this code

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.stick0 = wpilib.Joystick(0)
        self.stick1 = wpilib.Joystick(1)
        
        self.frontLeft = ctre.WPI_VictorSPX(11)
        self.midLeft = ctre.WPI_TalonSRX(10)
        self.rearLeft = ctre.WPI_VictorSPX(12)
        
        self.frontRight = ctre.WPI_VictorSPX(21)
        self.midRight = ctre.WPI_TalonSRX(20)
        self.rearRight = ctre.WPI_VictorSPX(22)
        
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.midLeft, self.rearLeft)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.midRight, self.rearRight)
        
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

    def teleopPeriodic(self):
        self.drive.tankDrive(self.stick0.getY(hand=None),self.stick1.getY(hand=None),squaredInputs=True)

if __name__ == '__main__':
    wpilib.run(MyRobot)
