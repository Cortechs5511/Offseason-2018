import wpilib

from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.buttons import Button
from wpilib.buttons import Trigger

from wpilib import XboxController as Xbox

from commands.setFixedWrist import setFixedWrist
from commands.setFixedLift import setFixedLift
from commands.setFixedIntake import setFixedIntake

from commands.setPositionWrist import setPositionWrist
from commands.setPositionLift import setPositionLift

from commands.setSpeedLift import setSpeedLift
from commands.setSpeedWrist import setSpeedWrist

import commands.Sequences as seq

from commands.crash import Crash

class axisButton(Trigger):

    def __init__(self, f, num, Threshold):
        self.f = f
        self.num = num
        self.Threshold = Threshold

    def get(self):
        return abs(self.f(self.num)) > self.Threshold


def getJoystick(num):
    '''
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    '''

    joystick0 = Joystick(0)
    joystick1 = Joystick(1)
    xbox = Xbox(2)

    if num == 0: return joystick0
    elif num == 1: return joystick1
    else: return xbox

def commands():
    joystick0 = getJoystick(0)
    joystick1 = getJoystick(1)
    xbox = getJoystick(2)

    button01 = JoystickButton(joystick0, 1)
    button01.whenPressed(seq.ExchangeShoot())
    button02 = JoystickButton(joystick0, 2)
    button02.whenPressed(seq.IntakePosition())
    button03 = JoystickButton(joystick0, 3)
    button03.whenPressed(seq.ExchangePosition())
    button04 = JoystickButton(joystick0, 4)
    button04.whenPressed(seq.ExchangePosition())

    button11 = JoystickButton(joystick1, 1)
    button11.whenPressed(seq.SwitchShoot())
    button12 = JoystickButton(joystick1, 2)
    button12.whenPressed(seq.SwitchPosition())
    button13 = JoystickButton(joystick1, 3)
    button13.whenPressed(seq.ProtectPosition())
    button14 = JoystickButton(joystick1, 4)
    button14.whenPressed(seq.ProtectPosition())

    x = JoystickButton(xbox, 1)
    x.whenPressed(setPositionWrist(-20))
    b = JoystickButton(xbox, 2)
    b.whenPressed(setPositionWrist(50))
    y = JoystickButton(xbox, 3)
    y.whenPressed(setPositionWrist(105))

    '''
    axis0 = axisButton(xbox.getY, 0, 0.1)
    axis0.whileActive(setFixedLift(xbox.getY(0)))
    axis1 = axisButton(xbox.getX, 1, 0.1)
    axis1.whileActive(setFixedWrist(xbox.getX(1)))
    trigger0 = axisButton(xbox.getTriggerAxis, 0, 0.1)
    trigger0.whileActive(setFixedIntake(xbox.getTriggerAxis(0)))
    trigger1 = axisButton(xbox.getTriggerAxis, 1, 0.1)
    trigger1.whileActive(setFixedIntake(-xbox.getTriggerAxis(1)))
'''

    axis0 = axisButton(xbox.getY, 0, 0.1)
    axis0.whileActive(setSpeedLift())
    axis1 = axisButton(xbox.getX, 1, 0.1)
    axis1.whileActive(setSpeedWrist())
    trigger0 = axisButton(xbox.getTriggerAxis, 0, 0.1)
    trigger0.whileActive(setFixedIntake(0.5))
    trigger1 = axisButton(xbox.getTriggerAxis, 1, 0.1)
    trigger1.whileActive(setFixedIntake(-0.5))
