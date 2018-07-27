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
    DTMode = 3 #1 = Complex Tank, 2 = Simple Tank, 3 = Complex Arcade, 4 = Simple Arcade
    printEnc = True

    # Pathfinder constants
    MAX_VELOCITY = 10 # ft/s
    MAX_ACCELERATION = 6

    def robotInit(self):
        self.setPeriod(0.02) #20 milliseconds

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

        self.drivetrain = DT.Drivetrain(self.motorsDT,self.encodersDT)

        self.navx = navx.AHRS.create_spi()

        self.robot_drive = wpilib.RobotDrive(self.motorsDT[0], self.motorsDT[1])

    def robotPeriodic(self):
        pass

    def autonomousInit(self):
        [left,right,modifier] = path.getTraj()

        leftFollower = pf.followers.EncoderFollower(left)
        leftFollower.configureEncoder(self.encodersDT[0].get(), helper.getPulsesPerRev(), helper.getWheelDiam())
        leftFollower.configurePIDVA(1.0, 0.0, 0.0, 1/helper.getMaxV(), 0)

        rightFollower = pf.followers.EncoderFollower(right)
        rightFollower.configureEncoder(self.encodersDT[1].get(), helper.getPulsesPerRev(), helper.getWheelDiam())
        rightFollower.configurePIDVA(1.0, 0.0, 0.0, 1/helper.getMaxV(), 0)

        self.leftFollower = leftFollower
        self.rightFollower = rightFollower

        # This code renders the followed path on the field in simulation (requires pyfrc 2018.2.0+)
        if wpilib.RobotBase.isSimulation():
            from pyfrc.sim import get_user_renderer
            renderer = get_user_renderer()
            if renderer:
                renderer.draw_pathfinder_trajectory(left, color='#0000ff', offset=(-1,0))
                renderer.draw_pathfinder_trajectory(modifier.source, color='#00ff00', show_dt=1.0, dt_offset=0.0)
                renderer.draw_pathfinder_trajectory(right, color='#0000ff', offset=(1,0))

    def autonomousPeriodic(self):

        l = self.leftFollower.calculate(self.encodersDT[0].get())
        r = self.rightFollower.calculate(self.encodersDT[1].get())

        #gyro_heading = -self.gyro.getAngle()    # Assuming the gyro is giving a value in degrees
        gyro_heading = -self.navx.getAngle()
        print([self.navx.isConnected(),self.navx.getAngle(),self.navx.getPitch(),self.navx.getYaw(),self.navx.getRoll()])
        desired_heading = pf.r2d(self.leftFollower.getHeading())   # Should also be in degrees

        # This is a poor man's P controller
        angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
        turn = 5 * (-1.0/80.0) * angleDifference

        l = l + turn
        r = r - turn

        # -1 is forward, so invert both values
        #self.drivetrain.tank(-l,r)
        self.robot_drive.tankDrive(-l, -r)

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
