#imports important packages for running
import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import math

#class of robot
class MyRobot(wpilib.TimedRobot):
    #declares the motors in existence
    def robotInit(self):
        self.Leftdrive1 = wpilib.VictorSP(0)
        self.Leftdrive2 = wpilib.VictorSP(1)
        self.Rightdrive1 = wpilib.VictorSP(2)
        self.Rightdrive2 = wpilib.VictorSP(3)

        self.leftJoystick = wpilib.Joystick(0)
        self.rightJoystick = wpilib.Joystick(1)
        self.left_encoder = wpilib.Encoder(0,1)

    def teleopInit(self):
        self.count = 0

    def autonomousInit(self):
    #creates a time to run
        self.count = 0
        self.autonTimer = wpilib.Timer()
        self.autonTimer.start()

    def autonomousPerodic(self):
        LeftDrive1.set(0.5)

    def teleopPeriodic(self):
        self.count+= 1
        sd.putNumber("Count",self.count)
        '''
        ticks = (self.left_encoder.getDistance())*255
        sd.putNumber("Ticks",ticks)

        distance = math.pi*4*ticks
        if ticks == 0:
            return 0
        else:
            encoderdistance = distance/ticks
        sd.putNumber("Encoder distance",encoderdistance)
        '''
        left = -(self.leftJoystick.getRawAxis(1))
        right = -(self.rightJoystick.getRawAxis(1))
        if abs(left) < 0.1:
            left = 0
        if abs(right) < 0.1:
            right = 0
        left = left*0.9
        right = right*0.9
        self.drive(left, right)


    def Leftdrivecontrol(self, leftPower):
        self.Leftdrive1.set(leftPower)
        self.Leftdrive2.set(leftPower)

    def Rightdrivecontrol(self, rightPower):
        self.Rightdrive1.set(rightPower)
        self.Rightdrive2.set(rightPower)

    def drive(self, leftPower,rightPower):
        self.Leftdrivecontrol(-leftPower)
        self.Rightdrivecontrol(rightPower)

if  __name__ == '__main__':
    wpilib.run(MyRobot)
