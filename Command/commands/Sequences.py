from wpilib.command import CommandGroup

from commands.setPositionWrist import setPositionWrist
from commands.setPositionLift import setPositionLift

from commands.setFixedLift import setFixedLift
from commands.setFixedIntake import setFixedIntake
from commands.setFixedIntake import setFixedIntake

from wpilib import SmartDashboard

class IntakePosition(CommandGroup):
    def __init__(self, maxtime=300):
        super().__init__('IntakePosition')
        self.addParallel(setPositionLift(0, maxtime))
        self.addParallel(setPositionWrist(110, maxtime))
        self.addParallel(setFixedIntake(-0.6, maxtime))

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def isFinished(self): return self.timer.get() > self.maxtime

'''
def IntakePosition(maxtime = 300):
    cg = CommandGroup("IntakePositon")
    cg.addParallel(setPositionLift(0, maxtime))
    cg.addParallel(setPositionWrist(110, maxtime))
    cg.addParallel(setFixedIntake(-0.6, maxtime))
    return cg
'''

class Level2IntakePosition(CommandGroup):
    def __init__(self, maxtime=300):
        super().__init__('Level2IntakePosition')
        self.addParallel(setPositionLift(10, maxtime))
        self.addParallel(setPositionWrist(110, maxtime))
        self.addParallel(setFixedIntake(-0.6, maxtime))

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def isFinished(self): return self.timer.get() > self.maxtime

'''
def Level2IntakePosition(maxtime = 300):
    cg = CommandGroup("Level2IntakePositon")
    cg.addParallel(setPositionLift(10, maxtime))
    cg.addParallel(setPositionWrist(110, maxtime))
    cg.addParallel(setFixedIntake(-0.6, maxtime))
    return cg
'''

class Level3IntakePosition(CommandGroup):
    def __init__(self, maxtime=300):
        super().__init__('Level3IntakePosition')
        self.addParallel(setPositionLift(20, maxtime))
        self.addParallel(setPositionWrist(110, maxtime))
        self.addParallel(setFixedIntake(-0.6, maxtime))

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def isFinished(self): return self.timer.get() > self.maxtime

'''
def Level3IntakePosition(maxtime = 300):
    cg = CommandGroup("Level3IntakePositon")
    cg.addParallel(setPositionLift(20, maxtime))
    cg.addParallel(setPositionWrist(110, maxtime))
    cg.addParallel(setFixedIntake(-0.6, maxtime))
    return cg
'''

class SwitchPosition(CommandGroup):
    def __init__(self, maxtime=300):
        super().__init__('SwitchPosition')
        self.addParallel(setPositionLift(25, maxtime))
        self.addParallel(setPositionWrist(90, maxtime))
        self.addParallel(setFixedIntake(-0.3, maxtime))

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def isFinished(self): return self.timer.get() > self.maxtime

'''
def SwitchPosition(maxtime = 300):
    cg = CommandGroup("SwitchPositon")
    cg.addParallel(setPositionLift(25, maxtime))
    cg.addParallel(setPositionWrist(90, maxtime))
    cg.addParallel(setFixedIntake(-0.3, maxtime))
    return cg
'''

class SwitchShoot(CommandGroup):
    def __init__(self, maxtime=300):
        super().__init__('SwitchShoot')
        self.addParallel(setPositionLift(25, maxtime))
        self.addParallel(setPositionWrist(90, maxtime))
        self.addParallel(setFixedIntake(0.6, maxtime))

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def isFinished(self): return self.timer.get() > self.maxtime

'''
def SwitchShoot(maxtime = 300):
    cg = CommandGroup("SwitchShoot")
    cg.addParallel(setPositionLift(25, maxtime))
    cg.addParallel(setPositionWrist(90, maxtime))
    cg.addParallel(setFixedIntake(0.6, maxtime))
    return cg
'''

class ExchangeShoot(CommandGroup):
    def __init__(self, maxtime=300):
        super().__init__('ExchangeShoot')
        self.addParallel(setPositionLift(0, maxtime))
        self.addParallel(setPositionWrist(110, maxtime))
        self.addParallel(setFixedIntake(0.8, maxtime))

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def isFinished(self): return self.timer.get() > self.maxtime

'''
def ExchangeShoot(maxtime = 300):
    cg = CommandGroup("ExchangeShoot")
    cg.addParallel(setPositionLift(0, maxtime))
    cg.addParallel(setPositionWrist(110, maxtime))
    cg.addParallel(setFixedIntake(0.8, maxtime))
    return cg
'''

class ExchangePosition(CommandGroup):
    def __init__(self, maxtime=300):
        super().__init__('ExchangePosition')
        self.addParallel(setPositionLift(0, maxtime))
        self.addParallel(setPositionWrist(110, maxtime))
        self.addParallel(setFixedIntake(-0.3, maxtime))

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def isFinished(self): return self.timer.get() > self.maxtime

'''
def ExchangePosition(maxtime = 300):
    cg = CommandGroup("ExchangePositon")
    cg.addParallel(setPositionLift(0, maxtime))
    cg.addParallel(setPositionWrist(110, maxtime))
    cg.addParallel(setFixedIntake(-0.3, maxtime))
    return cg
'''

class ProtectPosition(CommandGroup):
    def __init__(self, maxtime=300):
        super().__init__('ProtectPosition')
        self.addParallel(setFixedLift(-0.1, maxtime))
        self.addParallel(setPositionWrist(-20, maxtime))
        self.addParallel(setFixedIntake(-0.3, maxtime))

        self.timer = self.getRobot().timer
        self.maxtime = maxtime

    def isFinished(self): return self.timer.get() > self.maxtime

'''
def ProtectPosition(maxtime = 300):
    cg = CommandGroup("ProtectPosition")
    cg.addParallel(setFixedLift(-0.1, maxtime))
    cg.addParallel(setPositionWrist(-20, maxtime))
    cg.addParallel(setFixedIntake(-0.3, maxtime))
    return cg
'''

def UpdateDashboard():
    SmartDashboard.putData("IntakePosition", IntakePosition())
    SmartDashboard.putData("Level2IntakePosition",Level2IntakePosition())
    SmartDashboard.putData("Level3IntakePosition",Level3IntakePosition())
    SmartDashboard.putData("SwitchPositon",SwitchPosition())
    SmartDashboard.putData("SwitchShoot",SwitchShoot())
    SmartDashboard.putData("ExchangePositon",ExchangePosition())
    SmartDashboard.putData("ExchangeShoot",ExchangeShoot())
    SmartDashboard.putData("ProtectPosition",ProtectPosition())
