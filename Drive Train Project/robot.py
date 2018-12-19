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
        #self.rawdistance = self.left_encoder.get()
        #self.count+= 1
        #sd.putNumber("Count",self.count)
        #ticks = sd.getNumber("Ticks", 255)
        #radius = 4
        #distance = (2*math.pi*radius*self.rawdistance)
        #self.encoderdistance = distance/ticks
        #sd.putNumber("Encoderdistance",self.encoderdistance)

        self.drive(-self.leftJoystick.getRawAxis(1),self.rightJoystick.getRawAxis(1))

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
