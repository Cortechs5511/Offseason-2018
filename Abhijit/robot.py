#!/usr/bin/env python3

import wpilib
import mechanisms.drivetrain as DT
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
import wpilib.buttons

class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        
        TalonLeft = Talon(10)
        VictorLeft1 = Victor(11)
        VictorLeft2 = Victor(12)
        VictorLeft1.set(Victor.ControlMode.Follower,10)
        VictorLeft2.set(Victor.ControlMode.Follower,10)
        DTLeftMCs = [TalonLeft,VictorLeft1,VictorLeft2]
        
        TalonRight = Talon(20)
        VictorRight1 = Victor(21)
        VictorRight2 = Victor(22)
        VictorRight1.set(Victor.ControlMode.Follower,20)
        VictorRight2.set(Victor.ControlMode.Follower,20)
        DTRightMCs = [TalonRight,VictorRight1,VictorRight2]
        
        leftEncoder = wpilib.Encoder(0,1)
        rightEncoder = wpilib.Encoder(2,3)
        
        self.drivetrain = DT.Drivetrain(DTLeftMCs,DTRightMCs,leftEncoder,rightEncoder)

    def autonomousInit(self):
        self.drivetrain.auto_init()

    def teleopPeriodic(self):
        self.drivetrain.tank(self.leftStick.getY(),self.rightStick.getY())

    def testPeriodic(self):
        pass

if __name__ == '__main__':
    wpilib.run(MyRobot)