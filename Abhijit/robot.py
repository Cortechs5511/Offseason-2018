#!/usr/bin/env python3

import wpilib
import math
import numpy as np
import pathfinder as pf

import mechanisms.drivetrain as DT
import path.path as path
import helper.helper as helper
import dashboard.dash as dash

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
from robotpy_ext.common_drivers import navx
import wpilib.buttons

class MyRobot(wpilib.TimedRobot):
    DTMode = 1 #1 = Complex Tank, 2 = Simple Tank, 3 = Complex Arcade, 4 = Simple Arcade

    def robotInit(self):
        self.setPeriod(helper.getPeriod()) #20 milliseconds

        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)

        self.drivetrain = DT.Drivetrain()

        dash.init()

    def robotPeriodic(self):
        if(dash.getTime()%helper.getFreq()==0 and dash.getTime()>0):
            print('dsTime:', "{0:.0f}".format(dash.getTime()*helper.getPeriod()))
        dash.setTime(dash.getTime()+1)

    def autonomousInit(self):
        #self.drivetrain.initGetWheelbase()
        [self.leftFollower,self.rightFollower] = path.initPath(5,self.drivetrain)

    def autonomousPeriodic(self):
        #self.drivetrain.getWheelbase(1,10)
        path.followPath(self.drivetrain,self.leftFollower,self.rightFollower)

    def teleopInit(self):
        self.drivetrain.stop()
        self.drivetrain.encoders.reset()
        self.drivetrain.navx.disablePID()
        if(self.DTMode%2==0): self.drivetrain.simpleInit()

    def teleopPeriodic(self):
        if(self.DTMode==1): self.drivetrain.tank(self.leftStick.getY(),self.rightStick.getY())
        elif(self.DTMode==2): self.drivetrain.simpleTank(self.leftStick.getY(),self.rightStick.getY())
        elif(self.DTMode==3): self.drivetrain.arcade(self.leftStick.getY(),self.leftStick.getX())
        else: self.drivetrain.simpleArcade(self.leftStick.getX(),self.leftStick.getY())

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def disabledInit(self):
        self.drivetrain.stop()
        self.drivetrain.encoders.reset()

    def disabledPeriodic(self):
        self.drivetrain.stop()
        self.drivetrain.encoders.reset()

if __name__ == '__main__':
    wpilib.run(MyRobot)
