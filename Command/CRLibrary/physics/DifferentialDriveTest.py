import math

import CRLibrary
import CRLibrary.util.util as util
import CRLibrary.util.units as units
import CRLibrary.physics.DCMotorTransmission as DCMotorTransmission
import CRLibrary.physics.DifferentialDrive as DifferentialDrive

transmission = DCMotorTransmission.DCMotorTransmission(units.rpmToRadsPerSec(65), 0.35, 1.0)
drive = DifferentialDrive.DifferentialDrive(140.0, 84.0, 0, units.inchesToMeters(2.0), units.inchesToMeters(25.5)/2, transmission, transmission)

#dynamics = DifferentialDrive.DriveDynamics()
chassisVelocity = DifferentialDrive.ChassisState(units.feetToMeters(10), units.degreesToRadians(45))
chassisAcceleration = DifferentialDrive.ChassisState(units.feetToMeters(2), units.degreesToRadians(9))

wheelVelocity = DifferentialDrive.WheelState(5, 4)
wheelAcceleration = DifferentialDrive.WheelState(3, 2)

voltage = DifferentialDrive.WheelState(12, 0)

drive.solveForwardDynamics_CS(chassisVelocity, voltage).print()
drive.solveForwardDynamics_WS(wheelVelocity, voltage).print()
drive.solveInverseDynamics_CS(chassisVelocity, chassisAcceleration).print()
drive.solveInverseDynamics_WS(wheelVelocity, wheelAcceleration).print()

print(drive.getMaxAbsVelocity(0.2, 0, 10))
