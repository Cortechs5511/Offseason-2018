#!/usr/bin/env python3

import wpilib
import math

from wpilib.command import Command
from wpilib.drive import DifferentialDrive

from commandbased import CommandBasedRobot
from commands.autonomous import AutonomousProgram

from commands.setPositionWrist import setPositionWrist
from commands.setPositionLift import setPositionLift

from commands.setFixedDT import setFixedDT
from commands.setFixedIntake import setFixedIntake
from commands.setFixedLift import setFixedLift
from commands.setFixedWrist import setFixedWrist

from commands.setSpeedDT import setSpeedDT
from commands.DriveStraightTime import DriveStraightTime
from commands.DriveStraightDistance import DriveStraightDistance
from commands.TurnAngle import TurnAngle
from commands.DriveStraightTimePID import DriveStraightTimePID
from commands.DriveStraightDistancePID import DriveStraightDistancePID
#from commands.TurnAnglePID import TurnAnglePID

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

        SmartDashboard.putData("setPositionWrist", setPositionWrist(0,True))
        SmartDashboard.putData("setPositionLift", setPositionLift(0, True))

        SmartDashboard.putData("setFixedDT", setFixedDT())
        SmartDashboard.putData("setFixedIntake", setFixedIntake())
        SmartDashboard.putData("setFixedLift", setFixedLift())
        SmartDashboard.putData("setFixedWrist", setFixedWrist())

        SmartDashboard.putData("setSpeedDT", setSpeedDT())

        SmartDashboard.putData("DriveStraightDistance", DriveStraightDistance())
        SmartDashboard.putData("DriveStraightTime", DriveStraightTime())
        SmartDashboard.putData("TurnAngle", TurnAngle())

        SmartDashboard.putData("DriveStraightDistance", DriveStraightDistancePID())
        SmartDashboard.putData("DriveStraightTime", DriveStraightTimePID())
        #SmartDashboard.putData("TurnAngle", TurnAnglePID())

        Sequences.UpdateDashboard()

        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''
        self.joystick0 = oi.getJoystick(0)
        self.joystick1 = oi.getJoystick(1)
        self.xbox = oi.getJoystick(2)

        oi.commands()

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

        SmartDashboard.putData("Drive", self.drive)
        SmartDashboard.putData("Intake", self.intake)
        SmartDashboard.putData("Lift", self.lift)
        SmartDashboard.putData("Wrist", self.wrist)

if __name__ == '__main__':
    wpilib.run(MyRobot)
