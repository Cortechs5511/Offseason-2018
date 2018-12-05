#!/usr/bin/env python3
#
# This is a very simple robot program that can be used to send telemetry to
# the data_logger script to characterize your drivetrain. If you wish to use
# your actual robot code, you only need to implement the simple logic in the
# autonomousPeriodic function and change the NetworkTables update rate
#
# See http://robotpy.readthedocs.io/en/stable/install/robot.html for RobotPy
# installation instructions
#

import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import wpilib
from wpilib.drive import DifferentialDrive

from networktables import NetworkTables
from networktables.util import ntproperty


class MyRobot(wpilib.TimedRobot):
    '''Main robot class'''

    # NetworkTables API for controlling this

    #: Speed to set the motors to
    autospeed = ntproperty('/robot/autospeed', defaultValue=0, writeDefault=True)

    #: Test data that the robot sends back
    telemetry = ntproperty('/robot/telemetry', defaultValue=(0,)*9, writeDefault=False)

    prior_autospeed = 0

    WHEEL_DIAMETER = 0.5
    ENCODER_PULSE_PER_REV = 360

    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        timeout = 0

        TalonLeft = Talon(10)
        TalonRight = Talon(20)
        TalonLeft.setSafetyEnabled(False)
        TalonRight.setSafetyEnabled(False)

        if not wpilib.RobotBase.isSimulation():
            VictorLeft1 = Victor(11)
            VictorLeft2 = Victor(12)
            VictorLeft1.follow(TalonLeft)
            VictorLeft2.follow(TalonLeft)

            VictorRight1 = Victor(21)
            VictorRight2 = Victor(22)
            VictorRight1.follow(TalonRight)
            VictorRight2.follow(TalonRight)

            for motor in [VictorLeft1,VictorLeft2,VictorRight1,VictorRight2]:
                motor.clearStickyFaults(timeout)
                motor.setSafetyEnabled(False)
                motor.setInverted(True)

        for motor in [TalonLeft,TalonRight]:
            motor.setInverted(True)
            motor.setSafetyEnabled(False)
            motor.clearStickyFaults(timeout) #Clears sticky faults

            motor.configContinuousCurrentLimit(15,timeout) #15 Amps per motor
            motor.configPeakCurrentLimit(20,timeout) #20 Amps during Peak Duration
            motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(12,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

            motor.configOpenLoopRamp(0.2,timeout) #number of seconds from 0 to 1

        TalonRight.setInverted(False)
        if not wpilib.RobotBase.isSimulation():
            VictorRight1.setInverted(False)
            VictorRight2.setInverted(False)

        self.left = TalonLeft
        self.right = TalonRight

        self.leftEncoder = wpilib.Encoder(0,1)
        self.leftEncoder.setDistancePerPulse(4/12 * math.pi / 255)
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(2,3)
        self.rightEncoder.setDistancePerPulse(-4/12 * math.pi / 127)
        self.rightEncoder.setSamplesToAverage(10)

        self.drive = DifferentialDrive(self.left, self.right)
        self.drive.setSafetyEnabled(False)
        self.drive.setDeadband(0)

        #
        # Configure encoder related functions -- getpos and getrate should return
        # ft and ft/s
        #

        self.l_encoder_getpos = self.leftEncoder.getDistance
        self.l_encoder_getrate = self.leftEncoder.getRate

        self.r_encoder_getpos = self.rightEncoder.getDistance
        self.r_encoder_getrate = self.rightEncoder.getRate

        # Set the update rate instead of using flush because of a NetworkTables bug
        # that affects ntcore and pynetworktables
        # -> probably don't want to do this on a robot in competition
        NetworkTables.setUpdateRate(0.010)

    def disabledInit(self):
        self.logger.info("Robot disabled")
        self.drive.tankDrive(0, 0)

    def disabledPeriodic(self):
        pass

    def robotPeriodic(self):
        # feedback for users, but not used by the control program
        sd = wpilib.SmartDashboard
        sd.putNumber('l_encoder_pos', self.l_encoder_getpos())
        sd.putNumber('l_encoder_rate', self.l_encoder_getrate())
        sd.putNumber('r_encoder_pos', self.r_encoder_getpos())
        sd.putNumber('r_encoder_rate', self.r_encoder_getrate())

    def teleopInit(self):
        self.logger.info("Robot in operator control mode")

    def teleopPeriodic(self):
        self.drive.arcadeDrive(-self.lstick.getY(), -self.rstick.getY())

    def autonomousInit(self):
        self.logger.info("Robot in autonomous mode")

    def autonomousPeriodic(self):
        '''
            If you wish to just use your own robot program to use with the data
            logging program, you only need to copy/paste the logic below into
            your code and ensure it gets called periodically in autonomous mode

            Additionally, you need to set NetworkTables update rate to 10ms using
            the setUpdateRate call.

            Note that reading/writing self.autospeed and self.telemetry are
            NetworkTables operations (using pynetworktables's ntproperty), so
            if you don't read/write NetworkTables in your implementation it won't
            actually work.
        '''

        # Retrieve values to send back before telling the motors to do something
        now = wpilib.Timer.getFPGATimestamp()

        l_encoder_position = self.l_encoder_getpos()
        l_encoder_rate = self.l_encoder_getrate()

        r_encoder_position = self.r_encoder_getpos()
        r_encoder_rate = self.r_encoder_getrate()

        battery = self.ds.getBatteryVoltage()
        motor_volts = battery * abs(self.prior_autospeed)

        l_motor_volts = motor_volts
        r_motor_volts = motor_volts

        # Retrieve the commanded speed from NetworkTables
        autospeed = self.autospeed
        self.prior_autospeed = autospeed

        # command motors to do things
        self.drive.tankDrive(autospeed, autospeed, False)

        # send telemetry data array back to NT
        self.telemetry = (now,
                          battery,
                          autospeed,
                          l_motor_volts,
                          r_motor_volts,
                          l_encoder_position,
                          r_encoder_position,
                          l_encoder_rate,
                          r_encoder_rate)


if __name__ == '__main__':
    wpilib.run(MyRobot)
