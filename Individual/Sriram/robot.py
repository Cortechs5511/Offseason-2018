import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        #Inititializing left and right intake
        self.Intake1 = ctre.WPI_TalonSRX(50)
        self.Intake2 = ctre.WPI_TalonSRX(51)
        #Left intake follows right intake
        self.Intake2.follow(self.Intake1)

        #Inititializing left and right joysticks
        self.LeftJoy = wpilib.Joystick(1)
        self.RightJoy = wpilib.Joystick(0);

        #Initializing talons and victors
        self.DriveRight1 = ctre.WPI_TalonSRX(20)
        self.DriveLeft1 = ctre.WPI_TalonSRX(10)
        self.DriveRight2 =ctre.WPI_VictorSPX(21)
        self.DriveLeft2 =ctre.WPI_VictorSPX(11)
        self.DriveRight3 =ctre.WPI_VictorSPX(22)
        self.DriveLeft3 =ctre.WPI_VictorSPX(12)

        #Making the Victors follow Talons
        self.DriveRight2.follow(self.DriveRight1)
        self.DriveLeft3.follow(self.DriveRight1)
        self.DriveLeft2.follow(self.DriveLeft1)
        self.DriveLeft3.follow(self.DriveLeft1)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        self.DriveRight1.set(0.5)


    def teleopInit(self):
        self.count = 0

    def teleopPeriodic(self):
        self.count += 1
        sd.putNumber("count", self.count)

        #if you press button 1 (trigger) on the left joystick, do outtake
        if (self.LeftJoy.getRawButton(1)):
            self.Intake1.set(-0.7)
        #if you press button 1 (trigger) on the right joystick, do intake
        elif (self.RightJoy.getRawButton(1)):
            self.Intake1.set(0.7)
        #if you aren't pressing any buttons, keep the intake at 0 power
        else:
            self.Intake1.set(0.0)

        #if you press button 5 on right joystick, drive forward at .5 power
        if (self.RightJoy.getRawButton(5)):
            self.drive(0.5,0.5)
        #if you press button 6 on right joystick, drive backward at .5 power
        elif (self.RightJoy.getRawButton(6)):
            self.drive(-0.5,-0.5)
        #if you aren't pressing any buttons, use the joysticks to control the left and right motors
        else:
            #negative because the directions are inverted
            LeftPower = -self.LeftJoy.getRawAxis(1)
            RightPower = -self.RightJoy.getRawAxis(1)
            self.drive(LeftPower,RightPower)

    def drive(self, powerLeft, powerRight):
        #sets the driving power
        """positive = forward"""
        self.DriveRight1.set(-powerRight)
        self.DriveLeft1.set(-powerLeft)


if __name__ == '__main__':
    wpilib.run(MyRobot)
