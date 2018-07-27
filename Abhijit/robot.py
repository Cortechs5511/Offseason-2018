#!/usr/bin/env python3

import wpilib
import math
import numpy as np
import pathfinder as pf

import mechanisms.drivetrain as DT
import path.path as path
import helper.helper as helper

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
from robotpy_ext.common_drivers import navx
import wpilib.buttons

class MyRobot(wpilib.TimedRobot):
    DTMode = 1 #1 = Complex Tank, 2 = Simple Tank, 3 = Complex Arcade, 4 = Simple Arcade
    printEnc = False

    if wpilib.RobotBase.isSimulation():
        # These PID parameters are used in simulation
        kP = 0.05
        kI = 0.00
        kD = 0.15
        kF = 0.00
    else:
        # These PID parameters are used on a real robot
        kP = 0.03
        kI = 0.00
        kD = 0.00
        kF = 0.00

    kToleranceDegrees = 5.0

    def robotInit(self):
        self.setPeriod(helper.getPeriod()) #20 milliseconds

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

        distPerPulse = helper.getDistPerPulse()

        leftEncoder = wpilib.Encoder(0,1)
        rightEncoder = wpilib.Encoder(2,3)
        self.encodersDT = [leftEncoder,rightEncoder]

        for encoder in self.encodersDT:
            encoder.setDistancePerPulse(distPerPulse)
            encoder.setSamplesToAverage(10)

        self.navx = navx.AHRS.create_spi()

        self.drivetrain = DT.Drivetrain(self.motorsDT,self.encodersDT,self.navx)

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        turnController = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.navx, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnController.setContinuous(True)

        self.turnController = turnController
        self.rotateToAngleRate = 0
        self.turnController.enable()

        [left,right,modifier] = path.getTraj()
        gains = [2,0,1,1/helper.getMaxV(),0]

        leftFollower = pf.followers.EncoderFollower(left)
        leftFollower.configureEncoder(self.encodersDT[0].get(), helper.getPulsesPerRev(), helper.getWheelDiam())
        leftFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

        rightFollower = pf.followers.EncoderFollower(right)
        rightFollower.configureEncoder(self.encodersDT[1].get(), helper.getPulsesPerRev(), helper.getWheelDiam())
        rightFollower.configurePIDVA(gains[0],gains[1],gains[2],gains[3],gains[4])

        self.leftFollower = leftFollower
        self.rightFollower = rightFollower

        path.showPath(left,right,modifier)

    def autonomousPeriodic(self):
        l = self.leftFollower.calculate(self.encodersDT[0].get())
        r = self.rightFollower.calculate(self.encodersDT[1].get())

        gyro_heading = -self.navx.getYaw() #degrees
        desired_heading = pf.r2d(self.leftFollower.getHeading()) #degrees

        self.turnController.setSetpoint(desired_heading)
        turn = self.rotateToAngleRate
        l = l + turn
        r = r - turn

        self.drivetrain.tank(-l,r)

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output

    def teleopInit(self):
        self.drivetrain.stop()
        self.drivetrain.clearEncoders()
        if(self.DTMode%2==0):
            self.drivetrain.simpleInit()

    def teleopPeriodic(self):
        if(self.DTMode==1): self.drivetrain.tank(self.leftStick.getY(),self.rightStick.getY())
        elif(self.DTMode==2): self.drivetrain.simpleTank(self.leftStick.getY(),self.rightStick.getY())
        elif(self.DTMode==3): self.drivetrain.arcade(self.leftStick.getY(),self.leftStick.getX())
        else: self.drivetrain.simpleArcade(self.leftStick.getX(),self.leftStick.getY())

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
