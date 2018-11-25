#model of a DC motor rotating a shaft. All parameters refer to the output
#should already consider gearing and efficiency losses
#The motor is assumed symmetric forward/reverse

import CRLibrary
import CRLibrary.util.util as util
import CRLibrary.util.units as units

class DCMotorTransmission:
    __speedPerVolt__ = 0 #rad/s per V (no load)
    __torquePerVolt__ = 0 #N m per V (stall)
    __frictionVoltage__ = 0 #V

    def __init__(self, speedPerVolt, torquePerVolt, frictionVoltage):
        self.__speedPerVolt__ = speedPerVolt
        self.__torquePerVolt__ = torquePerVolt
        self.__frictionVoltage__ = frictionVoltage

    def speedPerVolt(self):
        return self.__speedPerVolt__

    def torquePerVolt(self):
        return self.__torquePerVolt__

    def frictionVoltage(self):
        return self.__frictionVoltage__

    def freeSpeedAtV(self, voltage):
        if(voltage>util.kEpsilon):
            return max(0, voltage - self.frictionVoltage()) * self.speedPerVolt()
        elif(voltage<-util.kEpsilon):
            return min(0, voltage + self.frictionVoltage()) * self.speedPerVolt()
        else:
            return 0

    def getTorqueForVoltage(self, outputSpeed, voltage):
        effVoltage = voltage
        if(outputSpeed>util.kEpsilon):
            effVoltage -= self.frictionVoltage()
        elif(outputSpeed<-util.kEpsilon):
            effVoltage += self.frictionVoltage()
        elif(voltage>util.kEpsilon):
            effVoltage = max(0, voltage-self.frictionVoltage())
        elif(voltage<-util.kEpsilon):
            effVoltage = min(0, voltage+self.frictionVoltage())
        else:
            return 0
        return self.torquePerVolt() * (-outputSpeed/self.speedPerVolt()+effVoltage)

    def getVoltageForTorque(self, outputSpeed, torque):
        frictionVoltage = 0
        if(outputSpeed>util.kEpsilon):
            frictionVoltage = self.frictionVoltage()
        elif(outputSpeed<-util.kEpsilon):
            frictionVoltage = -self.frictionVoltage()
        elif(torque>util.kEpsilon):
            frictionVoltage = self.frictionVoltage()
        elif(torque<-util.kEpsilon):
            frictionVoltage = -self.frictionVoltage()
        else:
            return 0
        return torque/self.torquePerVolt() + outputSpeed/self.speedPerVolt() + frictionVoltage
