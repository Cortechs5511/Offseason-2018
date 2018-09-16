#!/usr/bin/env python3

import wpilib
import math

from wpilib.command import Command
from wpilib.drive import DifferentialDrive

from commandbased import CommandBasedRobot
from commands.autonomous import AutonomousProgram

from commands import setPositionWrist
from commands import setPositionLift

from commands import setFixedDT
from commands import setFixedIntake
from commands import setFixedLift
from commands import setFixedWrist

from commands import setSpeedDT
from commands import setSpeedIntake
from commands import setSpeedLift
from commands import setSpeedWrist
from commands import DriveStraightTime
from commands import DriveStraightDistance
from commands import TurnAngle
from commands import Sequences

from subsystems import Wrist, Intake, Lift, Drive
import oi

from wpilib import SmartDashboard

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

        self.drive = Drive.Drive()
        self.lift = Lift.Lift()
        self.wrist = Wrist.Wrist()
        self.intake = Intake.Intake()

        self.autonomousProgram = AutonomousProgram()

        SmartDashboard.putData("setPositionWrist", setPositionWrist.setPositionWrist(0,True))
        SmartDashboard.putData("setPositionLift", setPositionLift.setPositionLift(0, True))
        SmartDashboard.putData("setFixedDT", setFixedDT.setFixedDT())
        SmartDashboard.putData("setFixedIntake", setFixedIntake.setFixedIntake())
        SmartDashboard.putData("setFixedLift", setFixedLift.setFixedLift())
        SmartDashboard.putData("setFixedWrist", setFixedWrist.setFixedWrist())
        SmartDashboard.putData("setSpeedDT", setSpeedDT.setSpeedDT())
        SmartDashboard.putData("setSpeedIntake", setSpeedIntake.setSpeedIntake())
        SmartDashboard.putData("setSpeedLift", setSpeedLift.setSpeedLift())
        SmartDashboard.putData("setSpeedWrist", setSpeedWrist.setSpeedWrist())
        SmartDashboard.putData("DriveStraightDistance", DriveStraightDistance.DriveStraightDistance())
        SmartDashboard.putData("DriveStraightTime", DriveStraightTime.DriveStraightTime())
        SmartDashboard.putData("TurnAngle", TurnAngle.TurnAngle())
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
        SmartDashboard.putNumber("WristPosition", math.degrees(self.wrist.getAngle()))
        SmartDashboard.putNumber("LiftPosition", self.lift.getHeight())
        SmartDashboard.putNumber("RightDistance", self.drive.getDistance()[0])
        SmartDashboard.putNumber("LeftDistance", self.drive.getDistance()[1])

        SmartDashboard.putNumber("DriveAmps",self.drive.getOutputCurrent())
        SmartDashboard.putNumber("IntakeAmps",self.intake.getOutputCurrent())
        SmartDashboard.putNumber("WristAmps", self.wrist.getOutputCurrent())
        SmartDashboard.putNumber("LiftAmps",self.lift.getOutputCurrent())

        total = self.drive.getOutputCurrent()+self.intake.getOutputCurrent()+self.wrist.getOutputCurrent()+self.lift.getOutputCurrent()
        SmartDashboard.putNumber("TotalAmps",total)

if __name__ == '__main__':
    wpilib.run(MyRobot)
