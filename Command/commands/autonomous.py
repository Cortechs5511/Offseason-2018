from wpilib.command.commandgroup import CommandGroup

from wpilib.command.waitcommand import WaitCommand

from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightTime import DriveStraightTime
from commands.TurnAngle import TurnAngle

from commands.DriveStraightDistancePID import DriveStraightDistancePID
from commands.DriveStraightTimePID import DriveStraightTimePID
from commands.TurnAnglePID import TurnAnglePID

import commands.Sequences as seq

from commands.setFixedDT import setFixedDT

from commands.Sequences import SwitchPosition
from commands.Sequences import SwitchShoot
from commands.Sequences import IntakePosition
from commands.Sequences import ProtectPosition
from commands.Sequences import ExchangePosition
from commands.Sequences import ExchangeShoot
from commands.setFixedWrist import setFixedWrist
from commands.setPositionWrist import setPositionWrist

class LeftSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__('LeftSwitchSide')
        self.addSequential(setFixedWrist(0.8, maxtime= 1))
        self.addParallel(SwitchPosition())
        self.addSequential(DriveStraightDistancePID((154/12.0), maxtime=6))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAnglePID(90, maxtime=10))
        self.addSequential(DriveStraightDistancePID(20/12.0, maxtime=12))
        self.addSequential(SwitchShoot())

class RightSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__('RightSwitchSide')
        self.addSequential(setFixedWrist(0.8, maxtime= 1))
        self.addSequential(setPositionWrist(100, False, maxtime=2.5))
        self.addSequential(SwitchPosition(maxtime=3))
        self.addSequential(DriveStraightDistancePID((154/12.0), maxtime=6))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAnglePID(-90, maxtime=10))
        self.addSequential(DriveStraightDistancePID(20/12.0, maxtime=12))
        self.addSequential(SwitchShoot())

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__('DriveStraight')
        self.addSequential(DriveStraightDistancePID(154/12.0, maxtime=5))
        self.addParallel(ProtectPosition())

class LeftSwitchMiddle2Cube(CommandGroup):
    def __init__(self):
        super().__init__('LeftSwitchMiddle2Cube')
        self.addSequential(setFixedWrist(0.8, maxtime= 1))
        self.addSequential(SwitchPosition(maxtime=1))
        self.addSequential(DriveStraightDistancePID(9.5/12.0, maxtime=2))
        self.addParallel(SwitchPosition(maxtime=2))
        self.addSequential(TurnAnglePID(-60, maxtime=3))
        self.addSequential(DriveStraightDistancePID(125/12.0, maxtime=6))
        self.addSequential(TurnAnglePID(0, maxtime=7))
        self.addSequential(DriveStraightDistancePID(36/12.0, maxtime=8))
        self.addSequential(SwitchShoot(maxtime=8))
        self.addSequential(DriveStraightDistancePID(-30/12, maxtime=9))
        self.addSequential(TurnAnglePID(45, maxtime=10))
        self.addParallel(IntakePosition(maxtime=10))
        self.addSequential(DriveStraightDistancePID(30/12, maxtime=11))
        self.addParallel(IntakePosition(maxtime=11))
        self.addSequential(DriveStraightDistancePID(-30/12, maxtime=12))
        self.addParallel(SwitchPosition(maxtime=12))
        self.addSequential(TurnAnglePID(0, maxtime=13))
        self.addParallel(SwitchPosition(maxtime=13))
        self.addSequential(DriveStraightDistancePID(30/12, maxtime=14))
        self.addSequential(SwitchShoot(maxtime=15))

class LeftSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__('LeftSwitchMiddle')
        self.addSequential(setFixedWrist(0.8, maxtime= 1))
        self.addSequential(SwitchPosition(maxtime=1))
        self.addSequential(DriveStraightDistancePID(9.5/12.0, maxtime=2))
        self.addParallel(SwitchPosition())
        self.addSequential(TurnAnglePID(-60, maxtime=5))
        self.addSequential(DriveStraightDistancePID(125/12.0, maxtime=11))
        self.addSequential(TurnAnglePID(0, maxtime=11))
        self.addSequential(DriveStraightDistancePID(36/12.0, maxtime=13))
        self.addSequential(SwitchShoot())

class RightSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__('RightSwitchMiddle')
        self.addSequential(setFixedWrist(0.8, maxtime= 1))
        self.addSequential(SwitchPosition(maxtime=3))
        self.addSequential(DriveStraightDistancePID(112/12.0))
        self.addParallel(SwitchPosition())
        self.addSequential(SwitchShoot())

class RightSwitchMiddle2Cube(CommandGroup):
    def __init__(self):
        super().__init__('RightSwitchMiddle2Cube')
        self.addSequential(setFixedWrist(0.8, maxtime= 1))
        self.addSequential(SwitchPosition(maxtime=1))
        self.addSequential(DriveStraightDistancePID(112/12.0, maxtime=4))
        self.addParallel(SwitchPosition(maxtime=4))
        self.addSequential(SwitchShoot(maxtime=5))
        self.addSequential(DriveStraightDistancePID(-30/12, maxtime=6))
        self.addSequential(TurnAnglePID(-45, maxtime=7))
        self.addParallel(IntakePosition(maxtime=7))
        self.addSequential(DriveStraightDistancePID(30/12, maxtime=8))
        self.addParallel(IntakePosition (maxtime=8))
        self.addSequential(DriveStraightDistancePID(-30/12, maxtime=9))
        self.addParallel(SwitchPosition(maxtime=9))
        self.addSequential(TurnAnglePID(0, maxtime=10))
        self.addParallel(SwitchPosition(maxtime=10))
        self.addSequential(DriveStraightDistancePID(30/12, maxtime=12))
        self.addSequential(SwitchShoot(maxtime=14))
