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
from commands.setFixedWrist import setFixedWrist

from commands.setSpeedDT import setSpeedDT
from commands.setSpeedLift import setSpeedLift
from commands.setSpeedWrist import setSpeedWrist

from commands.Zero import Zero

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

        #self.updateDashboardInit()

        oi.commands()


    '''def updateDashboardInit(self):
        #Subsystems
        SmartDashboard.putData("Drive", self.drive)
        SmartDashboard.putData("Intake", self.intake)
        SmartDashboard.putData("Lift", self.lift)
        SmartDashboard.putData("Wrist", self.wrist)

        #Commands
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

        #Additional UpdateDashboard Functions
        Sequences.UpdateDashboard()
        autonomous.UpdateDashboard()'''

    def updateDashboardPeriodic(self):
        current = self.drive.getOutputCurrent()+self.intake.getOutputCurrent()+self.wrist.getOutputCurrent()+self.lift.getOutputCurrent()
        SmartDashboard.putNumber("Total_Amps",current)

        SmartDashboard.putBoolean("Mech_Safety", (self.lift.lift.get() > 0.2 and self.wrist.getAngle() < math.pi/12))

        '''Additional UpdateDashboard Functions'''
        '''self.drive.UpdateDashboard()
        self.lift.UpdateDashboard()
        self.wrist.UpdateDashboard()
        self.intake.UpdateDashboard()'''

if __name__ == '__main__':
    wpilib.run(MyRobot)
