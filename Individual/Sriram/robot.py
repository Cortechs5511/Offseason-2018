import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.Intake1 = ctre.WPI_TalonSRX(50)
        self.Intake2 = ctre.WPI_TalonSRX(51)
        self.Intake2.follow(self.Intake1)
        self.LeftJoy = wpilib.Joystick(1)
        self.RightJoy = wpilib.Joystick(0);
        self.DriveRight1 = ctre.WPI_TalonSRX(20)
        self.DriveLeft1 = ctre.WPI_TalonSRX(10)
        self.DriveRight2 =ctre.WPI_VictorSPX(21)
        self.DriveLeft2 =ctre.WPI_VictorSPX(11)
        self.DriveRight3 =ctre.WPI_VictorSPX(22)
        self.DriveLeft3 =ctre.WPI_VictorSPX(12)
        self.DriveRight2.follow(self.DriveRight1)
        self.DriveLeft3.follow(self.DriveRight1)
        self.DriveLeft2.follow(self.DriveLeft1)
        self.DriveLeft3.follow(self.DriveLeft1)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        self.DriveRight1.set(0.5)
        AxisPowers = wpilib.Joystick(2)

    def teleopInit(self):
        self.count = 0

    def teleopPeriodic(self):
        self.count += 1
        sd.putNumber("count", self.count)
        if (self.LeftJoy.getRawButton(1)):
            self.Intake1.set(-0.7)
        elif (self.RightJoy.getRawButton(1)):
            self.Intake1.set(0.7)
        else:
            self.Intake1.set(0.0)
        if (self.RightJoy.getRawButton(5)):
            self.drive(0.5,0.5)
        elif (self.RightJoy.getRawButton(6)):
            self.drive(-0.5,-0.5)
        else:
            LeftPower = -self.LeftJoy.getRawAxis(1)
            RightPower = -self.RightJoy.getRawAxis(1)
            self.drive(LeftPower,RightPower)

    def drive(self, powerLeft, powerRight):

        """positive = forward"""
        self.DriveRight1.set(-powerRight)
        self.DriveLeft1.set(-powerLeft)

        west = AxisPowers.getAxis(5)
        self.Intake1.set(west)

if __name__ == '__main__':
    wpilib.run(MyRobot)
