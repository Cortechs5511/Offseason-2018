import math
import wpilib
import oi

from wpilib import SmartDashboard
import wpilib.buttons

from wpilib.command import Command
from commandbased import CommandBasedRobot

from commands.setPositionWrist import setPositionWrist
from commands.setPositionLift import setPositionLift

from commands.setFixedDT import setFixedDT
from commands.setFixedIntake import setFixedIntake
from commands.setFixedLift import setFixedLift
from commands.setFixedWrist import setFixedWrist

from commands.setSpeedDT import setSpeedDT
from commands.setSpeedLift import setSpeedLift
from commands.setSpeedWrist import setSpeedWrist

from commands.DriveStraightTime import DriveStraightTime
from commands.DriveStraightDistance import DriveStraightDistance
from commands.TurnAngle import TurnAngle

from commands.getLimelightData import getLimelightData

from commands.Zero import Zero

from commands import Sequences

from commands import autonomous
from commands.autonomous import LeftSwitchSide
from commands.autonomous import RightSwitchSide
from commands.autonomous import DriveStraight
from commands.autonomous import LeftSwitchMiddle
from commands.autonomous import RightSwitchMiddle
from commands.autonomous import LeftSwitchMiddle2Cube
from commands.autonomous import RightSwitchMiddle2Cube


from subsystems import Wrist, Intake, Lift, Drive

import pathfinder as pf
import path.path as path

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
from navx import AHRS as navx

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
        self.getLimelightData = getLimelightData()

        oi.commands()

        SmartDashboard.putString("position", "L")

        self.curr = 0
        self.print = 50

    def robotPeriodic(self):
        self.curr = self.curr + 1
        if(self.curr%self.print==0):
            self.updateDashboardPeriodic()
            self.curr = 0

    def autonomousInit(self):
        self.getLimelightData.start()
        self.wrist.zero()
        self.lift.zero()
        self.drive.zero()

        self.timer.reset()
        self.timer.start()

        gameData = "RLR" #wpilib.DriverStation.getInstance().getGameSpecificMessage()
        position = "L" #SmartDashboard.getString("position", "M")
        self.autoMode = self.autoLogic(gameData, position)

        if self.autoMode == "DriveStraight": self.DriveStraight.start()
        elif self.autoMode == "LeftSwitchSide": self.LeftSwitchSide.start()
        elif self.autoMode == "LeftSwitchMiddle": self.LeftSwitchMiddle.start()
        elif self.autoMode == "RightSwitchSide": self.RightSwitchSide.start()
        elif self.autoMode == "RightSwitchMiddle": self.RightSwitchMiddle.start()
        self.autoMode = "Nothing"

    def autonomousPeriodic(self):
        if self.autoMode == "Nothing":
            gameData = "LRL" #wpilib.DriverStation.getGameSpecificMessage()
            position = "M" #SmartDashboard.getString("position", "M")
            self.autoMode = self.autoLogic(gameData, position)

            if self.autoMode == "DriveStraight": self.DriveStraight.start()
            elif self.autoMode == "LeftSwitchSide": self.LeftSwitchSide.start()
            elif self.autoMode == "LeftSwitchMiddle": self.LeftSwitchMiddle2Cube.start()
            elif self.autoMode == "RightSwitchSide": self.RightSwitchSide.start()
            elif self.autoMode == "RightSwitchMiddle": self.RightSwitchMiddle2Cube.start()

        SmartDashboard.putString("AutoMode", self.autoMode)

        #path.pathFinder(self.drive)
        super().autonomousPeriodic()

    def autoLogic(self, gameData, auto):
        if(auto=="L"):
            if(gameData[0]=='L'): return "LeftSwitchSide"
            else: return "DriveStraight"
        elif(auto=="M"):
            if(gameData[0]=='L'): return "LeftSwitchMiddle"
            else: return "RightSwitchMiddle"
        elif(auto=="R"):
            if(gameData[0]=='L'): return "DriveStraight"
            else: return "RightSwitchSide"
        return "Nothing"

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
        SmartDashboard.putData("setSpeedLift", setSpeedLift())
        SmartDashboard.putData("setSpeedWrist", setSpeedWrist())

        SmartDashboard.putData("DriveStraightDistance", DriveStraightDistance())
        SmartDashboard.putData("DriveStraightTime", DriveStraightTime())
        SmartDashboard.putData("TurnAngle", TurnAngle())

        SmartDashboard.putData("Zero", Zero())

        '''Additional UpdateDashboard Functions'''
        Sequences.UpdateDashboard()
        autonomous.UpdateDashboard()

    def updateDashboardPeriodic(self):
        current = self.drive.getOutputCurrent()+self.intake.getOutputCurrent()+self.wrist.getOutputCurrent()+self.lift.getOutputCurrent()
        SmartDashboard.putNumber("Total_Amps",current)

        SmartDashboard.putBoolean("Mech_Safety", (self.lift.lift.get() > 0.2 and self.wrist.getAngle() < math.pi/12))

        '''Additional UpdateDashboard Functions'''
        self.drive.UpdateDashboard()
        self.lift.UpdateDashboard()
        self.wrist.UpdateDashboard()
        self.intake.UpdateDashboard()

if __name__ == '__main__':
    wpilib.run(MyRobot)
