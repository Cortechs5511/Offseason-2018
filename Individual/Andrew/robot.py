#imports important packages for running
import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre

#class of robot
class MyRobot(wpilib.TimedRobot):
    #declares the motors in existence
    def robotInit(self):
        
        #Intake motors
        self.Intake1 = ctre.WPI_TalonSRX(50)
        self.Intake2 = ctre.WPI_TalonSRX(51)
        self.Intake2.follow(self.Intake1)
        #drive motors
        self.LeftDrive1 = ctre.WPI_TalonSRX(10)
        self.LeftDrive2 = ctre.WPI_VictorSPX(11)
        self.LeftDrive3 = ctre.WPI_VictorSPX(12)
        self.LeftDrive3.follow(self.LeftDrive1)
        self.LeftDrive2.follow(self.LeftDrive1)

        self.RightDrive1 = ctre.WPI_TalonSRX(20)
        self.RightDrive2 = ctre.WPI_VictorSPX(21)
        self.RightDrive3 = ctre.WPI_VictorSPX(22)
        self.RightDrive3.follow(self.LeftDrive1)
        self.RightDrive2.follow(self.LeftDrive1)
        #setup for wrist
        self.Wrist = ctre.WPI_TalonSRX(40)
        #creates two axis' for teleop
        self.Axis = wpilib.Joystick(2)
        self.Rotate = wpilib.Joystick(1)

    def teleopInit(self):
        self.count = 0

    def teleopPeriodic(self):
        #teleoporated period; man control
        self.count += 1
        #puts the count variable on the SmartDashboard
        sd.putNumber("count", self.count)
        #sets the intake of the wrist to a speed
        west = self.Axis.getRawAxis(5)
        self.Intake1.set(west)
        #sets the angle of the wrist to a joystick
        up = self.Rotate.getRawAxis(1)
        self.Wrist.set(up)

    def disabledPeriodic(self):
        # a disabled period will reset the wrist and intake
        self.Wrist.set(0)
        self.Intake1.set(0)

    def autonomousInit(self):
        #creates a time to run
        self.count = 0
        self.autonTimer = wpilib.Timer()
        self.autonTimer.start()

    def autonomousPeriodic(self):
        self.count += 1
        #add count to SD
        sd.putNumber("count", self.count)
        # self.Wrist.set(-0.2)
        timeElapsed = self.autonTimer.get()
        sd.putNumber("Timer",timeElapsed)

        if timeElapsed < 2.75:
            # starts robot at left and right motor speeds of 0.4
            self.drive(0.4, 0.4)
        elif timeElapsed < 3:
            self.drive(0.5, 0.2)
        elif timeElapsed <4:
            self.drive(0.2,0.2)
        else:
            self.drive(0,0)

        if timeElapsed > 5:
            self.Output()
        elif timeElapsed >10:
            self.Input()
        else:
            self.disabledPeriodic

    def Output(self):
        self.Intake1.set(-0.2)
    def Input(self):
        self.Intake1.set(0.2)

    def drive(self, leftPower, rightPower):
        #IMPORTANT
        #Set your powers to positive to go forward, and negative for backward
        self.LeftDrive1.set(-leftPower)
        self.RightDrive1.set(-rightPower)
if __name__ == '__main__':
    wpilib.run(MyRobot)
