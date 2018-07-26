#!/usr/bin/env python3

import wpilib
import math
import numpy as np

#Any helper functions required over multiple files

def sign(x):
    if(x<0):
        return -1
    elif(x>0):
        return 1
    else:
        return 0
