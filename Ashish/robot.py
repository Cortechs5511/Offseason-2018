import wpilib
import wpilib.drive
import ctre

#I, Ashish, wrote this code

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.stick0 = wpilib.Joystick(0)
        self.stick1 = wpilib.Joystick(1)
        self.box = wpilib.XboxController(2)
        
        self.frontLeft = ctre.WPI_VictorSPX(11)
        self.midLeft = ctre.WPI_TalonSRX(10)
        self.rearLeft = ctre.WPI_VictorSPX(12)
        self.frontLeft.set(ctre.WPI_VictorSPX.ControlMode.Follower,10)
        self.rearLeft.set(ctre.WPI_VictorSPX.ControlMode.Follower,10)
        
        self.frontRight = ctre.WPI_VictorSPX(21)
        self.midRight = ctre.WPI_TalonSRX(20)
        self.rearRight = ctre.WPI_VictorSPX(22)
        self.frontRight.set(ctre.WPI_VictorSPX.ControlMode.Follower,20)
        self.rearRight.set(ctre.WPI_VictorSPX.ControlMode.Follower,20)
        
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.midLeft, self.rearLeft)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.midRight, self.rearRight)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.Lift30 = ctre.WPI_TalonSRX(30)
        self.Lift31 = ctre.WPI_TalonSRX(31)
        self.Wrist = ctre.WPI_TalonSRX(40)
        self.Intake50 = ctre.WPI_TalonSRX(50)
        self.Intake51 = ctre.WPI_TalonSRX(51)

        self.midLeft.configNeutralDeadband(0.04,0)
        self.midRight.configNeutralDeadband(0.04,0)

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        if self.timer.get() < 3.0:
            self.drive.tankDrive(0.5,0.5,squaredInputs=True)
        else:
            self.drive.tankDrive(0.0,0.0,squaredInputs=True)

    def teleopPeriodic(self):
        self.drive.tankDrive(self.stick0.getY(hand=None),self.stick1.getY(hand=None),squaredInputs=True)
        
        if self.box.getYButton() == True:
            self.Lift30.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,-0.6)
            self.Lift31.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,-0.6)
        elif self.box.getAButton() == True:
            self.Lift30.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,0.5)
            self.Lift31.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,0.5)
        else:
            pass
        
        if self.box.getXButton() == True:
            self.Wrist.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,0.3)
        elif self.box.getBButton() == True:
            self.Wrist.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,-0.3)
        else:
            pass

        if self.box.getStartButton() == True:
            self.Intake50.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,0.6)
            self.Intake51.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,0.6)
        elif self.box.getBackButton() == True:
            self.Intake50.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,-0.7)
            self.Intake51.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,-0.7)
        else:
            pass

if __name__ == '__main__':
    wpilib.run(MyRobot)
