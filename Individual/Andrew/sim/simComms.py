encoderReset = False

def resetEncoders():
    global encoderReset
    encoderReset = True

def resetEncodersSim():
    global encoderReset
    encoderReset = False

def getEncoders():
    global encoderReset
    return encoderReset
