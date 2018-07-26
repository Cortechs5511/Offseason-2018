import wpilib
import math
from wpilib.command.subsystem import Subsystem

class Drivetrain(Subsystem):

    def __init__(self, left, right, leftEncoder, rightEncoder):
        self.left = left
        self.right = right
        self.leftEncoder = leftEncoder
        self.rightEncoder = rightEncoder

    def tank(self,left,right):
        dbLimit = 0.1
        k = -2
        maxSpeed = 0.85

        if(abs(left)<dbLimit):left = 0
        else: left = abs(left)/left*(math.e**(k*abs(left))-1) / (math.e**k-1)

        if(abs(right)<dbLimit): right = 0
        else: right = abs(right)/right*(math.e**(k*abs(right))-1) / (math.e**k-1)

        left *= maxSpeed
        right *= maxSpeed

        self.left.set(left)
        self.right.set(right)

    def arcade(self,throttle,turn):
        dbLimit = 0.1
        k = -2
        maxSpeed = 0.85

        left = 0
        right = 0

        if(throttle>dbLimit):
            throttle = sign(throttle)*(math.exp(k*abs(throttle))-1)/(math.exp(k)-1)
        else:
            throttle = 0

        if(turn>dbLimit):
            turn = sign(turn)*(math.exp(k*abs(turn))-1)/(math.exp(k)-1)
        else:
            turn = 0

        L0 = throttle + turn
        R0 = throttle - turn

        L1 = maxSpeed * L0/(max(abs(L0),abs(R0),1))
        R1 = maxSpeed * R0/(max(abs(L0),abs(R0),1))

        self.left.set(L1)
        self.right.set(R1)

    def clearEncoders(self):
        self.left_encoder.reset()
        self.right_encoder.reset()

    def stop(self):
        self.DTLeftMCs[0].set(0)
        self.DTRightMCs[0].set(0)
