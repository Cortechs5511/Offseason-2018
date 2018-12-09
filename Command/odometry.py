import math

from CRLibrary.util import units

x = 0
y = 0
angle = 0

rightVel = 0
leftVel = 0

def init():
    global x
    global y
    global angle
    global rightVel
    global leftVel

    x = 0
    y = 0
    angle = 0
    rightVel = 0
    leftVel = 0

def update(leftV, rightV, angleIn):
    global x
    global y
    global angle
    global rightVel
    global leftVel
    speed = (leftV+rightV)/2
    x += speed * 0.02 * math.cos(math.pi/180*angleIn)
    y += speed * 0.02 * math.sin(math.pi/180*angleIn)
    angle = angleIn
    rightVel = rightV
    leftVel = leftV

def display():
    global x
    global y
    global angle
    global rightVel
    global leftVel
    print([x,y,angle, rightVel, leftVel])

def get():
    global x
    global y
    global angle
    global rightVel
    global leftVel
    return [x,y,angle, rightVel, leftVel]

def getSI():
    [x, y, angle, rightVel, leftVel] = get()
    x = units.feetToMeters(x)
    y = units.feetToMeters(y)
    angle = units.degreesToRadians(angle)
    rightVel = units.feetToMeters(rightVel)
    leftVel = units.feetToMeters(leftVel)
    return [x, y, angle, rightVel, leftVel]
