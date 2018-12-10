from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from wpilib import SmartDashboard

from commands.DriveStraightCombined import DriveStraightCombined
from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightTime import DriveStraightTime
from commands.DrivePath import DrivePath
from commands.TurnAngle import TurnAngle

from commands.setFixedDT import setFixedDT

import commands.Sequences as seq
from commands.Sequences import SwitchPosition
from commands.Sequences import SwitchShoot
from commands.Sequences import IntakePosition
from commands.Sequences import ProtectPosition
from commands.Sequences import ExchangePosition
from commands.Sequences import ExchangeShoot
from commands.setFixedWrist import setFixedWrist
from commands.setPositionWrist import setPositionWrist

#PATHFINDER AUTOS

class LeftSwitchMiddlePath(CommandGroup):
    def __init__(self, follower):
        super().__init__("LeftSwitchMiddlePath")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addParallel(SwitchPosition(timeout=5))
        self.addSequential(DrivePath(name="LeftSwitch", follower=follower, timeout=5))
        self.addSequential(SwitchShoot(timeout=1))
        '''
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=0, timeout=2))
        self.addSequential(TurnAngle(45, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=45, timeout=2))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=45, timeout=2))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))
        '''

class RightSwitchMiddlePath(CommandGroup):
    def __init__(self, follower="PathFinder"):
        super().__init__("RightSwitchMiddlePath")
        self.addSequential(DrivePath(name="DriveStraight", follower=follower, timeout=15))

class LeftScalePath(CommandGroup):
    def __init__(self, follower="PathFinder"):
        super().__init__("LeftScalePath")
        self.addSequential(DrivePath(name="LeftScale", follower=follower, timeout=15))

class RightScalePath(CommandGroup):
    def __init__(self, follower="PathFinder"):
        super().__init__("RightScalePath")
        self.addSequential(DrivePath(name="RightScale", follower=follower, timeout=15))

class LeftOppositeScalePath(CommandGroup):
    def __init__(self, follower="PathFinder"):
        super().__init__("LeftOppositeScalePath")
        self.addSequential(DrivePath(name="LeftOppositeScale", follower=follower, timeout=15))

class RightOppositeScalePath(CommandGroup):
    def __init__(self, follower="PathFinder"):
        super().__init__("RightOppositeScalePath")
        self.addSequential(DrivePath(name="RightOppositeScale", follower=follower, timeout=15))

class TestPath(CommandGroup):
    def __init__(self, follower="PathFinder"):
        super().__init__("TestPath")
        self.addSequential(DrivePath(name="Test", follower=follower, timeout=15))

'''STANDARD AUTOS'''

class LeftSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__("LeftSwitchSide")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addParallel(SwitchPosition())
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(90, timeout=4))
        self.addSequential(DriveStraightCombined(distance=20/12.0, angle=90, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__("RightSwitchSide")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addParallel(SwitchPosition())
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(-90, timeout=4))
        self.addSequential(DriveStraightCombined(distance=20/12.0, angle=-90, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__("DriveStraight")
        self.addSequential(DriveStraightCombined(distance=154/12.0, angle=0, timeout=5))
        self.addParallel(ProtectPosition(timeout = 5))

class LeftSwitchMiddle2Cube(CommandGroup):
    def __init__(self):
        super().__init__("LeftSwitchMiddle2Cube")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=9.5/12.0, angle=0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(-60, timeout=1))
        self.addSequential(DriveStraightCombined(distance=110/12.0, angle=-60, timeout=4))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addSequential(DriveStraightCombined(distance=36/12.0, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=0, timeout=2))
        self.addSequential(TurnAngle(45, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=45, timeout=2))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=45, timeout=2))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class LeftSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__("LeftSwitchMiddle")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=9.5/12.0, angle=0, timeout=1))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAngle(-60, timeout=2))
        self.addSequential(DriveStraightCombined(distance=125/12.0, angle=-60, timeout=5))
        self.addSequential(TurnAngle(0, timeout=2))
        self.addSequential(DriveStraightCombined(distance=36/12.0, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__("RightSwitchMiddle")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=2))
        self.addSequential(DriveStraightCombined(distance=112/12.0, angle=0, timeout=4))
        self.addParallel(SwitchPosition())
        self.addSequential(SwitchShoot(timeout=1))

class RightSwitchMiddle2Cube(CommandGroup):
    def __init__(self):
        super().__init__("RightSwitchMiddle2Cube")
        self.addSequential(setFixedWrist(0.8, timeout= 1))
        self.addSequential(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=112/12.0, angle=0, timeout=4))
        self.addParallel(SwitchPosition(timeout=2))
        self.addSequential(SwitchShoot(timeout=1))
        self.addParallel(DriveStraightTime(speed=0, timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=0, timeout=2))
        self.addSequential(DriveStraightTime(speed=0,timeout=1))
        self.addSequential(TurnAngle(-45, timeout=1))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=30/12, angle=-45, timeout=2))
        self.addParallel(IntakePosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=-30/12, angle=-45, timeout=2))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(TurnAngle(0, timeout=1))
        self.addParallel(SwitchPosition(timeout=1))
        self.addSequential(DriveStraightCombined(distance=42/12, angle=0, timeout=2))
        self.addSequential(SwitchShoot(timeout=1))

def UpdateDashboard():
    follower = "PathFinder"
    SmartDashboard.putData("LeftSwitchMiddlePath", LeftSwitchMiddlePath(follower))
    SmartDashboard.putData("RightSwitchMiddlePath", RightSwitchMiddlePath(follower))
    SmartDashboard.putData("LeftScalePath", LeftScalePath(follower))
    SmartDashboard.putData("RightScalePath", RightScalePath(follower))
    SmartDashboard.putData("LeftOppositeScalePath", LeftOppositeScalePath(follower))
    SmartDashboard.putData("RightOppositeScalePath", RightOppositeScalePath(follower))
    SmartDashboard.putData("TestPath", TestPath(follower))

    SmartDashboard.putData("LeftSwitchSide", LeftSwitchSide())
    SmartDashboard.putData("RightSwitchSide", RightSwitchSide())
    SmartDashboard.putData("DriveStraight", DriveStraight())
    SmartDashboard.putData("LeftSwitchMiddle", LeftSwitchMiddle())
    SmartDashboard.putData("RightSwitchMiddle", RightSwitchMiddle())
    SmartDashboard.putData("LeftSwitchMiddle2Cube", LeftSwitchMiddle2Cube())
    SmartDashboard.putData("RightSwitchMiddle2Cube", RightSwitchMiddle2Cube())
