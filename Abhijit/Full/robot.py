#!/usr/bin/env python3

import wpilib
import math
import numpy as np
import pathfinder as pf

import mechanisms.drivetrain as DT
import mechanisms.lift as lift
import mechanisms.wrist as wrist
import mechanisms.intake as intake

import path.path as path
import helper.helper as helper
import external.dash as dash
import external.ds as ds

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
        self.xbox = wpilib.XboxController(2)

        self.drivetrain = DT.Drivetrain()
        self.lift = lift.lift()
        self.wrist = wrist.wrist()
        self.intake = intake.intake()

        dash.init()
        ds.init()

    def robotPeriodic(self):
        '''
        if(dash.getTime()%helper.getFreq()==0 and dash.getTime()>0):
            print("Time:", "{0:.0f}".format(dash.getTime()*helper.getPeriod()))
        dash.setTime(dash.getTime()+1)
        '''

        helper.setAuto(dash.getAuto())
        helper.setGameData(ds.getGameData())

    def autonomousInit(self):
        #self.drivetrain.initGetWheelbase()
        pass

    def autonomousPeriodic(self):
        #self.drivetrain.getWheelbase(1,10)
        path.pathFinder(self.drivetrain)

    def teleopInit(self):
        self.drivetrain.stop()
        self.drivetrain.encoders.reset()
        self.drivetrain.disablePIDs()

        if(self.DTMode%2==0): self.drivetrain.simpleInit()

    def teleopPeriodic(self):
        if(self.DTMode==1): self.drivetrain.tank(self.leftStick.getY(),self.rightStick.getY())
        elif(self.DTMode==2): self.drivetrain.simpleTank(self.leftStick.getY(),self.rightStick.getY())
        elif(self.DTMode==3): self.drivetrain.arcade(self.leftStick.getY(),self.leftStick.getX())
        else: self.drivetrain.simpleArcade(self.leftStick.getX(),self.leftStick.getY())

        if(self.xbox.getAButton()):
            self.lift.setOut(0.7)
        elif(self.xbox.getBButton()):
            self.lift.setOut(-0.7)
        else:
            self.lift.stop()

        if(self.xbox.getXButton()):
            self.wrist.setOut(0.5)
        elif(self.xbox.getYButton()):
            self.wrist.setOut(-0.5)
        else:
            self.wrist.stop()

        if(self.xbox.getTriggerAxis(0)>0.5):
            self.intake.setOut(0.9)
        elif(self.xbox.getTriggerAxis(1)>0.5):
            self.intake.setOut(-0.9)
        else:
            self.intake.stop()

    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def disabledInit(self):
        self.drivetrain.stop()
        self.lift.stop()
        self.wrist.stop()
        self.intake.stop()

        self.drivetrain.disablePIDs()
        self.drivetrain.encoders.reset()

    def disabledPeriodic(self):
        self.drivetrain.stop()
        self.lift.stop()
        self.wrist.stop()
        self.intake.stop()

        self.drivetrain.disablePIDs()
        self.drivetrain.encoders.reset()

if __name__ == '__main__':
    wpilib.run(MyRobot)
