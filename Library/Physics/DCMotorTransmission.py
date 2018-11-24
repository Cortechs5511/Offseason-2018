#model of a DC motor rotating a shaft. All parameters refer to the output
#should already consider gearing and efficiency losses
#The motor is assumed symmetric forward/reverse

from ..Util import util

class DCMotorTransmission:
    __speedPerVolt__ #rad/s per V (no load)
    __torquePerVolt__ #N m per V (stall)
    __frictionVoltage__ #V

    def __init__(speedPerVolt, torquePerVolt, frictionVoltage):
        __speedPerVolt__ = speedPerVolt
        __torquePerVolt__ = torquePerVolt
        __frictionVoltage__ = frictionVoltage

    def getSpeedPerVolt():
        return __speedPerVolt__

    def getTorquePerVolt():
        return __torquePerVolt__

    def getFrictionVoltage():
        return __frictionVoltage__

    def freeSpeedAtV(voltage):
        if(voltage>util.kEpsilon):
            return max(0, voltage - getFrictionVoltage()) * getSpeedPerVolt()
        elif(voltage<-util.kEpsilon):
            return min(0, voltage + getFrictionVoltage()) * getSpeedPerVolt()
        else:
            return 0

    def getTorqueForVoltage(outputSpeed, voltage):
        effVoltage = voltage
        if(outputSpeed>util.kEpsilon):
            effVoltage -= getFrictionVoltage()
        elif(outputSpeed<-util.kEpsilon):
            effVoltage += getFrictionVoltage()
        elif(voltage>util.kEpsilon):
            effVoltage = max(0, voltage-getFrictionVoltage())
        elif(voltage<-util.kEpsilon):
            effVoltage = min(0, voltage+getFrictionVoltage())
        else:
            return 0
        return getTorquePerVolt() * (-outputSpeed/getSpeedPerVolt()+effVoltage)

    def getVoltageForTorque(outputSpeed, torque):
        frictionVoltage
        if(outputSpeed>util.kEpsilon):
            frictionVoltage = getFrictionVoltage()
        elif(outputSpeed<-util.kEpsilon):
            frictionVoltage = -getFrictionVoltage()
        elif(torque>util.kEpsilon):
            frictionVoltage = getFrictionVoltage()
        elif(torque<-util.kEpsilon):
            frictionVoltage = -getFrictionVoltage()
        else:
            return 0
        return torque/getTorquePerVolt() + outputSpeed/getSpeedPerVolt() + frictionVoltage
