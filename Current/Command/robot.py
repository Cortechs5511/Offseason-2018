#!/usr/bin/env python3

import wpilib
import math

from wpilib.command import Command
from wpilib.drive import DifferentialDrive

from commandbased import CommandBasedRobot
from commands.autonomous import AutonomousProgram
from commands import setPositionWrist
from commands import Sequences


from subsystems import Wrist, Intake, Lift, Drive
import oi
from wpilib import SmartDashboard
from networktables import NetworkTables

import pathfinder as pf
import path.path as path

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from robotpy_ext.common_drivers import navx

import wpilib.buttons

class MyRobot(CommandBasedRobot):

    def robotInit(self):
        '''
        This is a good place to set up your subsystems and anything else that
        you will need to access later.
        '''
        Command.getRobot = lambda x=0: self
        self.smartDashboard = NetworkTables.getTable("SmartDashboard")
        self.lift = Lift.Lift()
        self.wrist = Wrist.Wrist()
        self.intake = Intake.Intake()
        self.drive = Drive.Drive()
        self.autonomousProgram = AutonomousProgram()
        SmartDashboard.putData("WristCommand", setPositionWrist.setPositionWrist())
        Sequences.UpdateDashboard()



        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''
        self.joystick0 = oi.getJoystick(0)
        self.joystick1 = oi.getJoystick(1)
        self.xbox = oi.getJoystick(2)

    def autonomousInit(self):
        self.autonomousProgram.start()

    def robotPeriodic(self):
        self.smartDashboard.putNumber("WristPosition", self.wrist.getAngle())
        self.smartDashboard.putNumber("RawWristPosition", self.wrist.getRawPosition())
        self.smartDashboard.putNumber("LiftPosition", self.lift.getHeight())
        self.smartDashboard.putNumber("RightDistance", self.drive.encoders.getDistance()[0])
        self.smartDashboard.putNumber("LeftDistance", self.drive.encoders.getDistance()[1])

        self.smartDashboard.putNumber("DriveAmps",self.drive.getOutputCurrent())
        self.smartDashboard.putNumber("IntakeAmps",self.intake.getOutputCurrent())
        self.smartDashboard.putNumber("WristAmps", self.wrist.getOutputCurrent())
        self.smartDashboard.putNumber("LiftAmps",self.lift.getOutputCurrent())

if __name__ == '__main__':
    wpilib.run(MyRobot)
