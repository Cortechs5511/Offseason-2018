import math

from CRLibrary.util import units

[x, y, angle, rightVel, leftVel] = [0, 0, 0, 0, 0]

def init():
    global x, y, angle, rightVel, leftVel
    [x, y, angle, rightVel, leftVel] = [0, 0, 0, 0, 0]

def update(leftV, rightV, angleIn):
    global x, y, angle, rightVel, leftVel
    speed = (leftV+rightV)/2
    x += speed * 0.02 * math.cos(math.pi/180*angleIn)
    y += speed * 0.02 * math.sin(math.pi/180*angleIn)
    angle = angleIn
    rightVel = rightV
    leftVel = leftV

def getLeftVelocity(): return leftVel
def getRightVelocity(): return rightVel
def getAngle(): return angle

def get():
    global x, y, angle, rightVel, leftVel
    return [x,y,angle, leftVel, rightVel]

def getSI():
    [x, y, angle, rightVel, leftVel] = get()
    x = units.feetToMeters(x)
    y = units.feetToMeters(y)
    angle = units.degreesToRadians(angle)
    rightVel = units.feetToMeters(rightVel)
    leftVel = units.feetToMeters(leftVel)
    return [x, y, angle, leftVel, rightVel]

def display(): print(get())
