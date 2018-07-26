#!/usr/bin/env python3

import wpilib
import math
import numpy as np

from wpilib.command.subsystem import Subsystem
import helper.helper as helper

class Drivetrain(Subsystem):

    self.dbLimit = 0.1
    self.k = -2
    self.maxSpeed = 0.85

    def __init__(self, left, right, leftEncoder, rightEncoder):
        self.left = left
        self.right = right
        self.leftEncoder = leftEncoder
        self.rightEncoder = rightEncoder

    def setParams(dbLimit,k,maxSpeed):
        self.dbLimit = dbLimit
        self.k = k
        self.maxSpeed = maxSpeed

    def tank(self,left,right):
        if(abs(left)<dbLimit):left = 0
        else: left = abs(left)/left*(math.e**(k*abs(left))-1) / (math.e**k-1)

        if(abs(right)<dbLimit): right = 0
        else: right = abs(right)/right*(math.e**(k*abs(right))-1) / (math.e**k-1)

        left *= maxSpeed
        right *= maxSpeed

        self.left.set(left)
        self.right.set(right)

    def arcade(self,throttle,turn):
        left = 0
        right = 0

        if(abs(throttle)>dbLimit): throttle = np.sign(throttle)*(math.exp(k*abs(throttle))-1)/(math.exp(k)-1)
        else: throttle = 0

        if(abs(turn)>dbLimit): turn = np.sign(turn)*(math.exp(k*abs(turn))-1)/(math.exp(k)-1)
        else: turn = 0

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
        self.left.set(0)
        self.right.set(0)
