from wpilib.command.commandgroup import CommandGroup

from wpilib.command.waitcommand import WaitCommand

from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightTime import DriveStraightTime
from commands.TurnAngle import TurnAngle

from commands.DriveStraightDistancePID import DriveStraightDistancePID
from commands.DriveStraightTimePID import DriveStraightTimePID

class AutonomousProgram(CommandGroup):
    '''
    A simple program that spins the motor for two seconds, pauses for a second,
    and then spins it in the opposite direction for two seconds.
    '''

    def __init__(self):
        super().__init__('Autonomous Program')

        #self.addSequential(DriveStraightDistance(3))
        #self.addSequential(WaitCommand(1))
        #self.addSequential(DriveStraightTime(0.7, 2))

        #self.addSequential(DriveStraightDistancePID(10))
        self.addSequential(DriveStraightDistancePID(10))
        self.addSequential(TurnAngle(90))
