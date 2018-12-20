#imports important packages for running
import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre

#class of robot
class MyRobot(wpilib.TimedRobot):
#initialization
    def robotInit(self):
    #Intake motors
        self.Intake1 = ctre.WPI_TalonSRX(50)
        self.Intake2 = ctre.WPI_TalonSRX(51)
        #intake motors to follow each other
        self.Intake2.follow(self.Intake1)
    #leftdrive motors initialized
    #Sets the invert true; meaning it will go straight
    #Sets neutral mode to let robot coast
        self.LeftDrive1 = ctre.WPI_TalonSRX(10)
        self.LeftDrive1.setInverted(True)
        self.LeftDrive1.setNeutralMode(2)
        self.LeftDrive2 = ctre.WPI_VictorSPX(11)
        self.LeftDrive2.setInverted(True)
        self.LeftDrive2.setNeutralMode(2)
        self.LeftDrive3 = ctre.WPI_VictorSPX(12)
        self.LeftDrive3.setInverted(True)
        self.LeftDrive3.setNeutralMode(2)
    #sets motors to follow each other
        self.LeftDrive3.follow(self.LeftDrive1)
        self.LeftDrive2.follow(self.LeftDrive1)
    #rightdrive motors
        self.RightDrive1 = ctre.WPI_TalonSRX(20)
        self.RightDrive1.setInverted(True)
        self.RightDrive1.setNeutralMode(2)
        self.RightDrive2 = ctre.WPI_VictorSPX(21)
        self.RightDrive2.setInverted(True)
        self.RightDrive2.setNeutralMode(2)
        self.RightDrive3 = ctre.WPI_VictorSPX(22)
        self.RightDrive3.setInverted(True)
        self.RightDrive3.setNeutralMode(2)
    #sets motors to follow each other
        self.RightDrive3.follow(self.RightDrive1)
        self.RightDrive2.follow(self.RightDrive1)
    #setup for wrist
        self.Wrist = ctre.WPI_TalonSRX(40)
    #creates two joysticks for drive control
        self.left_drive = wpilib.Joystick(1)
        self.right_drive = wpilib.Joystick(0)
    #sets up encoders
        self.left_encoder = wpilib.Encoder(0,1)
        self.right_encoder = wpilib.Encoder(2,3)
    def teleopInit(self):
        self.count = 0
    def autonomousInit(self):
    #creates a time to run
        self.count = 0
        self.autonTimer = wpilib.Timer()
        self.autonTimer.start()

    def teleopPeriodic(self):
    #teleoporated period; man control
        self.count += 1
    #puts the count variable on the SmartDashboard
        sd.putNumber("count", self.count)
        self.ticks = self.getDistance()
        sd.putNumber("ticks",self.ticks)
    #limit breakers which set speeds based on axis units
        left = self.left_drive.getRawAxis(1)
        right = self.right_drive.getRawAxis(1)
        if abs(left) < 0.1:
            left = 0
        if abs(right) < 0.1:
            right = 0
        left = left *0.9
        right = right *0.9
        self.drive(left, right)

    def autonomousPeriodic(self):
        #Count and time on SD
        self.count += 1
        sd.putNumber("count", self.count)
        timeElapsed = self.autonTimer.get()
        sd.putNumber("Timer",timeElapsed)
        #runs forward function for 20 feet
        forwad(self,240,0.6)

#support functions
    #gets distance for ticks and converts
    def getDistance(self):
        left_ticks = (self.left_encoder.getDistance())/255
        right_ticks = (self.right_encoder.getDistance())/-127
        ticks = (left_ticks +right_ticks)/2
        distance = ticks * 4 *3.14
        return distance
#action functions
    #def turn (self,angle):

    def forward(self,maxSpeed,maxPoint):
        #constant for a linear decline
        constant = (maxSpeed/maxPoint)
        #variable for remaining distance
        remaining_distance = maxPoint - self.getDistance()
        #once this distance travelled is larger than the maxPoint, we know we've reached our goal, stopping it
        if self.getDistance <= maxPoint:
            self.drive(remaining_distance*constant+0.25,remaining_distance*constant+0.25)
        else:
            self.drive(0,0)
    def Output(self,outputPower):
        self.Intake1.set(-outputPower)
    def Input(self,inputPower):
        self.Intake1.set(inputPower)
    def drive(self, leftPower, rightPower):
        self.LeftDrive1.set(leftPower)
        self.RightDrive1.set(rightPower)
    def disabledPeriodic(self):
        # a disabled period will reset the wrist and intake
        self.Wrist.set(0)
        self.Intake1.set(0)
        self.drive(0,0)

#run code
if __name__ == '__main__':
    wpilib.run(MyRobot)
