#imports important packages for running
import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre
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


    def teleopPeriodic(self):
        self.rawdistance = left_encoder.getdistance()
        self.count+= 1
        sd.putNumber("Count",self.count)
        ticks = sd.getNumber("Ticks", 255)
        radius = 4
        distance = (2*math.pi*radius*self.rawdistance)
        self.encoderdistance = distance/ticks
        sd.putNumber("Encoderdistance",self.encoderdistance)


        left = self.leftJoystick.getRawAxis(1)
        right = self.rightJoystick.getRawAxis(1)
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
        self.Leftdrivecontrol(leftPower)
        self.Rightdrivecontrol(rightPower)

if  __name__ == '__main__':
    wpilib.run(MyRobot)