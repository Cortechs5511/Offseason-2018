import wpilib
import math
from wpilib.command.subsystem import Subsystem

class Drivetrain(Subsystem):
    
    def __init__(self, DTLeftMCs, DTRightMCs, leftEncoder, rightEncoder):
        self.DTLeftMCs = DTLeftMCs
        self.DTRightMCs = DTRightMCs
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
        
        self.DTLeftMCs[0].set(left)
        self.DTRightMCs[0].set(right)
        
    def clearEncoders(self):
        self.left_encoder.reset()
        self.right_encoder.reset()
        
    def stop(self):
        self.DTLeftMCs[0].set(0)
        self.DTRightMCs[0].set(0)