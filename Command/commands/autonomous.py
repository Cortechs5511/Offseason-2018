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

class LeftSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__('LeftSwitchSide')
        self.addSequential(DriveStraightDistancePID((154/12.0),True,6))
        self.addParallel(seq.SwitchPosition())
        self.addSequential(TurnAnglePID(90, True, 10))
        #self.addSequential(DriveStraightDistancePID(20/12.0))
        self.addSequential(seq.SwitchShoot())

class RightSwitchSide(CommandGroup):
    def __init__(self):
        super().__init__('RightSwitchSide')
        self.addSequential(DriveStraightDistancePID((154/12.0),True,6))
        self.addParallel(seq.SwitchPosition())
        self.addSequential(TurnAnglePID(-90, True))
        self.addSequential(DriveStraightDistancePID((12/12.0),True)
        self.addSequential(seq.SwitchShoot())

class DriveStraight(CommandGroup):
    def __init__(self):
        super().__init__('DriveStraight')
        self.addSequential(DriveStraightDistancePID(154/12.0))
        self.addParallel(seq.SwitchPosition())

class LeftSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__('LeftSwitchMiddle')
        self.addSequential(DriveStraightDistancePID(10/12.0))
        self.addParallel(seq.SwitchPosition())
        self.addSequential(TurnAnglePID(-50))
        self.addSequential(DriveStraightDistancePID(130/12.0))
        self.addSequential(TurnAnglePID(0))
        self.addSequential(DriveStraightDistancePID(10/12.0))
        self.addSequential(seq.SwitchShoot())

class RightSwitchMiddle(CommandGroup):
    def __init__(self):
        super().__init__('RightSwitchMiddle')
        self.addSequential(DriveStraightDistancePID(112/12.0))
        self.addParallel(seq.SwitchPosition())
        self.addSequential(seq.SwitchShoot())
