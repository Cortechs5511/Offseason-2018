from wpilib.command import CommandGroup

from commands.setPositionWrist import setPositionWrist
from commands.setPositionWrist90 import setPositionWrist90
from commands.setPositionLift import setPositionLift
from commands.setFixedLift import setFixedLift
from commands.setFixedIntake import setFixedIntake

from wpilib import SmartDashboard

class IntakePosition(CommandGroup):
    def __init__(self, timeout = 300):
        super().__init__('IntakePosition')
        self.addParallel(setPositionLift(0, timeout))
        self.addParallel(setPositionWrist90(timeout))
        self.addParallel(setFixedIntake(-0.6, timeout))

class Level2IntakePosition(CommandGroup):
    def __init__(self, timeout = 300):
        super().__init__('Level2IntakePosition')
        self.addParallel(setPositionLift(10, timeout))
        self.addParallel(setPositionWrist90(timeout))
        self.addParallel(setFixedIntake(-0.6, timeout))

class Level3IntakePosition(CommandGroup):
    def __init__(self, timeout = 300):
        super().__init__('Level3IntakePosition')
        self.addParallel(setPositionLift(20, timeout))
        self.addParallel(setPositionWrist90(timeout))
        self.addParallel(setFixedIntake(-0.6, timeout))

class SwitchPosition(CommandGroup):
    def __init__(self, timeout = 300):
        super().__init__('SwitchPosition')
        self.addParallel(setPositionLift(25, timeout))
        self.addParallel(setPositionWrist(90, timeout))
        self.addParallel(setFixedIntake(-0.3, timeout))

class SwitchShoot(CommandGroup):
    def __init__(self, timeout = 300):
        super().__init__('SwitchShoot')
        self.addParallel(setPositionLift(25, timeout))
        self.addParallel(setPositionWrist90(timeout))
        self.addParallel(setFixedIntake(0.7, timeout))

class ExchangeShoot(CommandGroup):
    def __init__(self, timeout = 300):
        super().__init__('ExchangeShoot')
        self.addParallel(setPositionLift(0, timeout))
        self.addParallel(setPositionWrist90(timeout))
        self.addParallel(setFixedIntake(0.8, timeout))

class ExchangePosition(CommandGroup):
    def __init__(self, timeout = 300):
        super().__init__('ExchangePosition')
        self.addParallel(setPositionLift(0, timeout))
        self.addParallel(setPositionWrist90(timeout))
        self.addParallel(setFixedIntake(-0.3, timeout))

class ProtectPosition(CommandGroup):
    def __init__(self, timeout = 300):
        super().__init__('ProtectPosition')
        self.addParallel(setFixedLift(-0.1, timeout))
        self.addParallel(setPositionWrist(-20, timeout))
        self.addParallel(setFixedIntake(-0.3, timeout))

def UpdateDashboard():
    SmartDashboard.putData("IntakePosition", IntakePosition())
    SmartDashboard.putData("Level2IntakePosition",Level2IntakePosition())
    SmartDashboard.putData("Level3IntakePosition",Level3IntakePosition())
    SmartDashboard.putData("SwitchPositon",SwitchPosition())
    SmartDashboard.putData("SwitchShoot",SwitchShoot())
    SmartDashboard.putData("ExchangePositon",ExchangePosition())
    SmartDashboard.putData("ExchangeShoot",ExchangeShoot())
    SmartDashboard.putData("ProtectPosition",ProtectPosition())
