#!/usr/bin/env python3

import wpilib
import math

from wpilib.command import Command
from wpilib.drive import DifferentialDrive

from commandbased import CommandBasedRobot
import commands.autonomous as auto

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

from commands.Zero import Zero


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

from sensors.DTEncoders import DTEncoders

class MyRobot(CommandBasedRobot):

    def robotInit(self):
        '''
        This is a good place to set up your subsystems and anything else that
        you will need to access later.
        '''

        Command.getRobot = lambda x=0: self

        self.drive = Drive.Drive(self)
        self.lift = Lift.Lift(self)
        self.wrist = Wrist.Wrist(self)
        self.intake = Intake.Intake(self)

        self.autonomousProgram = AutonomousProgram()

        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''
        self.joystick0 = oi.getJoystick(0)
        self.joystick1 = oi.getJoystick(1)
        self.xbox = oi.getJoystick(2)

        oi.commands()

        self.updateDashboardInit()

    def autonomousInit(self):
        self.autoMode = "Nothing"

    def autonomousPeriodic(self):
        if self.autoMode == "Nothing":
            gameData =
            position =
            self.autoMode = autoSelector.getName(autoSelector.calcNum(gameData, position))
            if self.autoMode == "DriveStraight":
                auto.DriveStraight().start()
            elif self.autoMode == "LeftSwitchSide":
                auto.LeftSwitchSide().start()
            elif self.autoMode == "LeftSwitchMiddle":
                auto.LeftSwitchMiddle().start()
            elif self.autoMode == "RightSwitchSide":
                auto.RightSwitchSide().start()
            elif self.autoMode == "RightSwitchMiddle":
                auto.RightSwitchMiddle().start()

    def robotPeriodic(self):
        self.updateDashboardPeriodic()




    def updateDashboardInit(self):
        '''Subsystems'''
        SmartDashboard.putData("Drive", self.drive)
        SmartDashboard.putData("Intake", self.intake)
        SmartDashboard.putData("Lift", self.lift)
        SmartDashboard.putData("Wrist", self.wrist)

        '''Commands'''
        SmartDashboard.putData("setPositionWrist", setPositionWrist(0,True))
        SmartDashboard.putData("setPositionLift", setPositionLift(0, True))

        SmartDashboard.putData("setFixedDT", setFixedDT())
        SmartDashboard.putData("setFixedIntake", setFixedIntake())
        SmartDashboard.putData("setFixedLift", setFixedLift())
        SmartDashboard.putData("setFixedWrist", setFixedWrist())

        SmartDashboard.putData("setSpeedDT", setSpeedDT())
        SmartDashboard.putData("setSpeedLift", setSpeedDT())
        SmartDashboard.putData("setSpeedWrist", setSpeedDT())

        SmartDashboard.putData("DriveStraightDistance", DriveStraightDistance())
        SmartDashboard.putData("DriveStraightTime", DriveStraightTime())
        SmartDashboard.putData("TurnAngle", TurnAngle())

        SmartDashboard.putData("DriveStraightDistance", DriveStraightDistancePID())
        SmartDashboard.putData("DriveStraightTime", DriveStraightTimePID())
        #SmartDashboard.putData("TurnAngle", TurnAnglePID())

        SmartDashboard.putData("Zero", Zero())

        '''Additional UpdateDashboard Functions'''
        Sequences.UpdateDashboard()

    def updateDashboardPeriodic(self):
        '''Sensor Output'''
        SmartDashboard.putNumber("WristPosition", math.degrees(self.wrist.getAngle()))
        SmartDashboard.putNumber("LiftPosition", self.lift.getHeight())
        SmartDashboard.putNumber("RightDistance", self.drive.getDistance()[0])
        SmartDashboard.putNumber("LeftDistance", self.drive.getDistance()[1])

        '''Current Logging'''
        SmartDashboard.putNumber("DriveAmps",self.drive.getOutputCurrent())
        SmartDashboard.putNumber("IntakeAmps",self.intake.getOutputCurrent())
        SmartDashboard.putNumber("WristAmps", self.wrist.getOutputCurrent())
        SmartDashboard.putNumber("LiftAmps",self.lift.getOutputCurrent())

        total = self.drive.getOutputCurrent()+self.intake.getOutputCurrent()+self.wrist.getOutputCurrent()+self.lift.getOutputCurrent()
        SmartDashboard.putNumber("TotalAmps",total)

        '''Additional UpdateDashboard Functions'''
        self.drive.UpdateDashboard()
        self.lift.UpdateDashboard()
        #self.wrist.UpdateDashboard()
        #self.intake.UpdateDashboard()



if __name__ == '__main__':
    wpilib.run(MyRobot)
