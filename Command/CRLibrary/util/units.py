import math

def rpmToRadsPerSec(rpm):
    return rpm * 2 * math.pi / 60

def radsPerSecToRPM(radsPerSec):
    return radsPerSec * 60 / (2 * math.pi)

def inchesToMeters(inches):
    return inches * 0.0254

def metersToInches(meters):
    return meters / 0.0254

def feetToMeters(feet):
    return inchesToMeters(feet * 12)

def metersToFeet(meters):
    return metersToInches(meters)/12

def degreesToRadians(degrees):
    return degrees * math.pi / 180

def radiansToDegrees(radians):
    return radians * 180 / math.pi

def poundsToKg(pounds):
    return pounds * 0.453592

def kgToPounds(kg):
    return kg * 2.20462
