#model of a DC motor rotating a shaft. All parameters refer to the output
#should already consider gearing and efficiency losses
#The motor is assumed symmetric forward/reverse

import util

class DCMotorTransmission:
    __speedPerVolt__ = 0 #rad/s per V (no load)
    __torquePerVolt__ = 0 #N m per V (stall)
    __frictionVoltage__ = 0 #V

    def __init__(self, speedPerVolt, torquePerVolt, frictionVoltage):
        self.__speedPerVolt__ = speedPerVolt
        self.__torquePerVolt__ = torquePerVolt
        self.__frictionVoltage__ = frictionVoltage

    def getSpeedPerVolt(self):
        return self.__speedPerVolt__

    def getTorquePerVolt(self):
        return self.__torquePerVolt__

    def getFrictionVoltage(self):
        return self.__frictionVoltage__

    def freeSpeedAtV(self, voltage):
        if(voltage>util.kEpsilon):
            return max(0, voltage - self.getFrictionVoltage()) * self.getSpeedPerVolt()
        elif(voltage<-util.kEpsilon):
            return min(0, voltage + self.getFrictionVoltage()) * self.getSpeedPerVolt()
        else:
            return 0

    def getTorqueForVoltage(self, outputSpeed, voltage):
        effVoltage = voltage
        if(outputSpeed>util.kEpsilon):
            effVoltage -= self.getFrictionVoltage()
        elif(outputSpeed<-util.kEpsilon):
            effVoltage += self.getFrictionVoltage()
        elif(voltage>util.kEpsilon):
            effVoltage = max(0, voltage-self.getFrictionVoltage())
        elif(voltage<-util.kEpsilon):
            effVoltage = min(0, voltage+self.getFrictionVoltage())
        else:
            return 0
        return self.getTorquePerVolt() * (-outputSpeed/self.getSpeedPerVolt()+effVoltage)

    def getVoltageForTorque(self, outputSpeed, torque):
        frictionVoltage = 0
        if(outputSpeed>util.kEpsilon):
            frictionVoltage = self.getFrictionVoltage()
        elif(outputSpeed<-util.kEpsilon):
            frictionVoltage = -self.getFrictionVoltage()
        elif(torque>util.kEpsilon):
            frictionVoltage = self.getFrictionVoltage()
        elif(torque<-util.kEpsilon):
            frictionVoltage = -self.getFrictionVoltage()
        else:
            return 0
        return torque/self.getTorquePerVolt() + outputSpeed/self.getSpeedPerVolt() + frictionVoltage
