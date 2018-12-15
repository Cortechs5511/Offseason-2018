import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre
import math
#import wpilib.Timer

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

        self.leftjoystick = wpilib.Joystick(0)
        self.rightjoystick = wpilib.Joystick(1)

        self.Lift1 = ctre.WPI_TalonSRX(30)
        self.Lift2 = ctre.WPI_TalonSRX(31)

        self.Intake1 = ctre.WPI_TalonSRX(50)
        self.Intake2 = ctre.WPI_TalonSRX(51)
        self.Intake2.follow(self.Intake1)

        #drive right
        self.driveleft1 = ctre.WPI_TalonSRX(10)
        self.driveleft2 = ctre.WPI_VictorSPX(11)
        self.driveleft3 = ctre.WPI_VictorSPX(12)
        self.driveleft2.follow(self.driveleft1)
        self.driveleft3.follow(self.driveleft1)
        #drive right
        self.driveright1 = ctre.WPI_TalonSRX(20)
        self.driveright2 = ctre.WPI_VictorSPX(21)
        self.driveright3 = ctre.WPI_VictorSPX(22)
        self.driveright2.follow(self.driveright1)
        self.driveright3.follow(self.driveright1)

        #teleop stuff
    def teleopDrive(self):
        leftthrottle=-self.leftjoystick.getRawAxis(1)
        rightthrottle=-self.rightjoystick.getRawAxis(1)
        self.drive(leftthrottle,rightthrottle)

    def teleopInit(self):
        self.count = 0

    def teleopPeriodic(self):
        self.count += 1
        sd.putNumber("count", self.count)


        self.teleopDrive()
        if self.leftjoystick.getButton(1):
            self.Intake1.set(0.5)
        elif self.rightjoystick.getButton(1):
            self.Intake1.set(-0.5)
        else: self.Intake1.set(0)

        if self.leftjoystick.getRawButton(3):
            self.Lift1.set(0.9)
        elif self.rightjoystick.getRawButton(3):
            self.Lift1.set(-0.9)
        else: self.Lift1.set(0)
    '''
    def autonomousPeriodic(self):
        if self.autonTimer.get()<4.0:
            self.drive(0.5, 0.5)
        else:
            self.drive(0,0)
    '''
    def drive(self,left,right):
        self.driveright1.set(-right)
        self.driveleft1.set(-left)

    def autonomousInit(self):
        self.leftAutonEncoder = wpilib.Encoder(0,1)
        self.autonTimer = wpilib.Timer()


        self.autonTimer.start()

    def autonomousPeriodic(self):
        encoderTicks = self.leftAutonEncoder.get()
        Wheelturn = encoderTicks / 255
        while Wheelturn < (10 / math.pi ) :
            self.drive(0.5,0.6)



if __name__ == '__main__':
    wpilib.run(MyRobot)
