import math

x = 0
y = 0
angle = 0

def init():
    global x
    global y
    global angle
    x = 0
    y = 0
    angle = 0

def update(leftVel, rightVel, angleIn):
    global x
    global y
    global angle
    speed = (leftVel+rightVel)/2
    x += speed * 0.02 * math.cos(math.pi/180*angleIn)
    y += speed * 0.02 * math.sin(math.pi/180*angleIn)
    angle = angleIn

def display():
    global x
    global y
    global angle
    print([x, y, angle])