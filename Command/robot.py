#!/usr/bin/env python3

import wpilib
import math
import autoSelector

from navx import AHRS as navx

from wpilib.command import Command
from wpilib.drive import DifferentialDrive

from commandbased import CommandBasedRobot
#from wpilib.command import Scheduler
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
from commands.TurnAnglePID import TurnAnglePID
from commands.DriveStraightTimePID import DriveStraightTimePID
from commands.DriveStraightDistancePID import DriveStraightDistancePID
#from commands.TurnAnglePID import TurnAnglePID



from commands.autonomous import LeftSwitchSide
from commands.autonomous import RightSwitchSide
from commands.autonomous import DriveStraight
from commands.autonomous import LeftSwitchMiddle
from commands.autonomous import RightSwitchMiddle
from commands.autonomous import LeftSwitchMiddle2Cube
from commands.autonomous import RightSwitchMiddle2Cube

from commands.Zero import Zero
from commands import Sequences

from subsystems import Wrist, Intake, Lift, Drive
import oi
import wpilib

from wpilib import SmartDashboard

import pathfinder as pf
import path.path as path

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import wpilib.buttons

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


        self.timer = wpilib.Timer()

        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''
        self.joystick0 = oi.getJoystick(0)
        self.joystick1 = oi.getJoystick(1)
        self.xbox = oi.getJoystick(2)

        self.updateDashboardInit()

        self.DriveStraight = DriveStraight()
        self.LeftSwitchSide = LeftSwitchSide()
        self.RightSwitchSide = RightSwitchSide()
        self.LeftSwitchMiddle = LeftSwitchMiddle()
        self.RightSwitchMiddle = RightSwitchMiddle()
        self.LeftSwitchMiddle2Cube = LeftSwitchMiddle2Cube()
        self.RightSwitchMiddle2Cube = RightSwitchMiddle2Cube()

        oi.commands()

        SmartDashboard.putString("position", "L")

        self.curr = 0
        self.print = 50

    def robotPeriodic(self):
        if(self.curr%self.print==0):
            self.updateDashboardPeriodic()

            self.curr = 0

        self.curr = self.curr + 1

    def autonomousInit(self):
        self.wrist.zero()
        self.lift.zero()
        self.drive.zero()
        self.timer.reset()
        self.timer.start()

        self.drive.zero()

        self.autoMode = "Nothing"

        gameData = "RLR" #wpilib.DriverStation.getInstance().getGameSpecificMessage()
        position = "L" #SmartDashboard.getString("position", "M")
        self.autoMode = autoSelector.calcNum(gameData, position)

        if self.autoMode == "DriveStraight": self.DriveStraight.start()
        elif self.autoMode == "LeftSwitchSide": self.LeftSwitchSide.start()
        elif self.autoMode == "LeftSwitchMiddle": self.LeftSwitchMiddle.start() #self.LeftSwitchMiddle.start()
        elif self.autoMode == "RightSwitchSide": self.RightSwitchSide.start()
        elif self.autoMode == "RightSwitchMiddle": self.RightSwitchMiddle.start() #self.RightSwitchMiddle.start()
        #Scheduler.enable(self)

        self.autoMode = "Nothing"

        if self.autoMode == "Nothing":

            gameData = "LLL"#wpilib.DriverStation.getInstance().getGameSpecificMessage()
            position = "M" #SmartDashboard.getString("position", "M")

            self.autoMode = autoSelector.calcNum(gameData, position)
            if self.autoMode == "DriveStraight": self.DriveStraight.start()
            elif self.autoMode == "LeftSwitchSide": self.LeftSwitchSide.start()
            elif self.autoMode == "LeftSwitchMiddle": self.LeftSwitchMiddle.start() #self.LeftSwitchMiddle.start()
            elif self.autoMode == "RightSwitchSide": self.RightSwitchSide.start()
            elif self.autoMode == "RightSwitchMiddle": self.RightSwitchMiddle.start() #self.RightSwitchMiddle.start()

    def autonomousPeriodic(self):
        if self.autoMode == "Nothing":
            gameData = "RLR" #wpilib.DriverStation.getGameSpecificMessage()
            self.autoMode = autoSelector.calcNum(gameData, position)

            if self.autoMode == "DriveStraight": self.DriveStraight.start()
            elif self.autoMode == "LeftSwitchSide": self.LeftSwitchSide.start()
            elif self.autoMode == "LeftSwitchMiddle": self.LeftSwitchMiddle.start() #self.LeftSwitchMiddle.start()
            elif self.autoMode == "RightSwitchSide": self.RightSwitchSide.start()
            elif self.autoMode == "RightSwitchMiddle": self.RightSwitchMiddle.start() #self.RightSwitchMiddle.start()

        SmartDashboard.putString("AutoMode", self.autoMode)

        super().autonomousPeriodic()

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
        SmartDashboard.putData("TurnAnglePID", TurnAnglePID(0,True))

        SmartDashboard.putData("DriveStraightDistance", DriveStraightDistancePID(10,True))
        SmartDashboard.putData("DriveStraightDistanceBack", DriveStraightDistancePID(-10))
        SmartDashboard.putData("DriveStraightTime", DriveStraightTimePID())
        #SmartDashboard.putData("TurnAngle", TurnAnglePID())

        SmartDashboard.putData("LeftSwitchSide", LeftSwitchSide())

        SmartDashboard.putData("Zero", Zero())

        '''Additional UpdateDashboard Functions'''
        #Sequences.UpdateDashboard()

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
