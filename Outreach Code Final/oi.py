import wpilib

from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.buttons import Button
from wpilib.buttons import Trigger

from wpilib import XboxController as Xbox

from commands.setFixedWrist import setFixedWrist
from commands.setFixedIntake import setFixedIntake

from commands.setPositionWrist import setPositionWrist
from commands.setPositionLift import setPositionLift

from commands.setSpeedLift import setSpeedLift
from commands.setSpeedWrist import setSpeedWrist

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

    x = JoystickButton(xbox, 1)
    x.whenPressed(setPositionWrist(-20, timeout=300))
    b = JoystickButton(xbox, 2)
    b.whenPressed(setPositionWrist(50, timeout=300))
    y = JoystickButton(xbox, 3)
    y.whenPressed(setPositionWrist(105, timeout=300))

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
    axis0.whileActive(setSpeedLift(timeout=300))
    axis1 = axisButton(xbox.getX, 1, 0.1)
    axis1.whileActive(setSpeedWrist(timeout=300))
    trigger0 = axisButton(xbox.getTriggerAxis, 0, 0.1)
    trigger0.whileActive(setFixedIntake(0.7, timeout=300))
    trigger1 = axisButton(xbox.getTriggerAxis, 1, 0.1)
    trigger1.whileActive(setFixedIntake(-0.7, timeout=300))
