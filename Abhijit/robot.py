#!/usr/bin/env python3

import wpilib
import math
import numpy as np

import mechanisms.drivetrain as DT

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
import wpilib.buttons

class MyRobot(wpilib.IterativeRobot):
    DTMode = 1 #1 = Complex Tank, 2 = Simple Tank, 3 = Complex Arcade, 4 = Simple Arcade
    printEnc = False

    def robotInit(self):
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)

        TalonLeft = Talon(10)
        VictorLeft1 = Victor(11)
        VictorLeft2 = Victor(12)
        VictorLeft1.set(Victor.ControlMode.Follower,10)
        VictorLeft2.set(Victor.ControlMode.Follower,10)
        self.DTLeftMCs = [TalonLeft,VictorLeft1,VictorLeft2]

        TalonRight = Talon(20)
        VictorRight1 = Victor(21)
        VictorRight2 = Victor(22)
        VictorRight1.set(Victor.ControlMode.Follower,20)
        VictorRight2.set(Victor.ControlMode.Follower,20)
        self.DTRightMCs = [TalonRight,VictorRight1,VictorRight2]

        self.motorsDT = [TalonLeft,TalonRight]

        distPerPulse = (4/12)*(2*math.pi)/127

        leftEncoder = wpilib.Encoder(0,1)
        rightEncoder = wpilib.Encoder(2,3)
        self.encodersDT = [leftEncoder,rightEncoder]

        for encoder in self.encodersDT:
            encoder.setDistancePerPulse(distPerPulse)
            encoder.setSamplesToAverage(10)

        self.drivetrain = DT.Drivetrain(self.motorsDT,self.encodersDT)

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.drivetrain.stop()
        self.drivetrain.clearEncoders()
        if(self.DTMode%2==0):
            self.drivetrain.simpleInit()

    def teleopPeriodic(self):
        if(self.DTMode==1):
            self.drivetrain.tank(self.leftStick.getY(),self.rightStick.getY())
        elif(self.DTMode==2):
            self.drivetrain.simpleTank(self.leftStick.getY(),self.rightStick.getY())
        elif(self.DTMode==3):
            self.drivetrain.arcade(self.leftStick.getY(),self.leftStick.getX())
        else:
            self.drivetrain.simpleArcade(self.leftStick.getX(),self.leftStick.getY())

        if(self.printEnc): self.drivetrain.printEncoders()

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def disabledInit(self):
        self.drivetrain.stop()
        self.drivetrain.clearEncoders()

    def disabledPeriodic(self):
        self.drivetrain.stop()
        self.drivetrain.clearEncoders()

if __name__ == '__main__':
    wpilib.run(MyRobot)
