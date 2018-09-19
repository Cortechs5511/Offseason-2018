import wpilib.buttons
from wpilib.drive import DifferentialDrive
import ctre


class MyRobot(wpilib.IterativeRobot):


    def __init__(self):
        super().__init__()
        # self.turn_power = 0
        self.Max_Speed = 0.85
        self.maxlift = 0.9
        self.kSlotIdx = 0
        self.kPIDLoopIdx = 0
        self.kTimeoutMs = 10
        self.Lift_F = 0
        self.Lift_P = 0
        self.Lift_I = 0
        self.Lift_D = 0
        self.LiftStickConstant = 4000

    def robotInit(self):
        '''Robot initialization function'''

        # object that handles basic drive operations
        self.DriveLeft1 = ctre.WPI_TalonSRX(10)
        self.DriveLeft2 = ctre.WPI_VictorSPX(11)
        self.DriveLeft3 = ctre.WPI_VictorSPX(12)
        self.DriveLeft2.set(ctre.WPI_VictorSPX.ControlMode.Follower, 10)
        self.DriveLeft3.set(ctre.WPI_VictorSPX.ControlMode.Follower, 10)

        self.DriveRight1 = ctre.WPI_TalonSRX(20)
        self.DriveRight2 = ctre.WPI_VictorSPX(21)
        self.DriveRight3 = ctre.WPI_VictorSPX(22)
        self.DriveRight2.set(ctre.WPI_VictorSPX.ControlMode.Follower, 20)
        self.DriveRight3.set(ctre.WPI_VictorSPX.ControlMode.Follower, 20)

        self.LeftEncoder = wpilib.Encoder(0, 1)
        self.RightEncoder = wpilib.Encoder(2, 3)

        self.left = wpilib.SpeedControllerGroup(self.DriveLeft1)
        self.right = wpilib.SpeedControllerGroup(self.DriveRight1)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        # intake
        self.Lintake = ctre.WPI_TalonSRX(50)
        self.Rintake = ctre.WPI_TalonSRX(51)
        self.Rintake.set(ctre.WPI_TalonSRX.ControlMode.Follower, 50)

        # lift
        self.Lift1 = ctre.WPI_TalonSRX(30)
        self.Lift2 = ctre.WPI_TalonSRX(31)
        self.Lift2.set(ctre.WPI_TalonSRX.ControlMode.Follower, 30)

        # wrist
        self.wrist = ctre.WPI_TalonSRX(40)

        # joysticks 1 & 2 on the driver station
        self.LeftJoystick = wpilib.Joystick(0)
        self.RightJoystick = wpilib.Joystick(1)
        self.cntrlr = wpilib.XboxController(2)

        self.loops = 0
        self.timesInMotionMagic = 0

        for talon in [ self.Lift1, self.Lift2 ]:
                # first choose the sensor
            talon.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative, self.kPIDLoopIdx, self.kTimeoutMs)
            talon.setSensorPhase(False)
            talon.setInverted(False)

            # Set relevant frame periods to be at least as fast as periodic rate
            talon.setStatusFramePeriod(ctre.WPI_TalonSRX.StatusFrameEnhanced.Status_13_Base_PIDF0, 10, self.kTimeoutMs)
            talon.setStatusFramePeriod(ctre.WPI_TalonSRX.StatusFrameEnhanced.Status_10_MotionMagic, 10, self.kTimeoutMs)

            # set the peak and nominal outputs
            talon.configNominalOutputForward(0, self.kTimeoutMs)
            talon.configNominalOutputReverse(0, self.kTimeoutMs)
            talon.configPeakOutputForward(self.maxlift, self.kTimeoutMs)
            talon.configPeakOutputReverse(self.maxlift * -1, self.kTimeoutMs)

            # set closed loop gains in slot0 - see documentation */
            talon.selectProfileSlot(self.kSlotIdx, self.kPIDLoopIdx)
            talon.config_kF(self.Lift_F, 0.2, self.kTimeoutMs)
            talon.config_kP(self.Lift_P, 0.2, self.kTimeoutMs)
            talon.config_kI(self.Lift_I, 0, self.kTimeoutMs)
            talon.config_kD(self.Lift_D, 0, self.kTimeoutMs)
            # set acceleration and vcruise velocity - see documentation
            talon.configMotionCruiseVelocity(15000, self.kTimeoutMs)
            talon.configMotionAcceleration(6000, self.kTimeoutMs)
            # zero the sensor
            talon.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)


    # def __init__(self, kp=1):
    # super().__init__()
    # self.turn_power = kp * (self.RightEncoder - self.LeftEncoder)

    def teleopInit(self):
        '''Executed at the start of teleop mode'''
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
        '''Runs the motors with tank steering'''
        self.myRobot.tankDrive((self.LeftJoystick.getY()) * -1 * self.Max_Speed,
                               (self.RightJoystick.getY()) * -1 * self.Max_Speed)

        if self.cntrlr.getYButton() == True:
            targetPos = self.cntrlr.getY(0) * self.LiftStickConstant
            self.Lift1.set(ctre.WPI_TalonSRX.ControlMode.MotionMagic, targetPos)
        else:
            self.Lift1.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput, self.cntrlr.getY(0))

        if self.cntrlr.getXButton() == True:
            self.wrist.set(-0.3)
        elif self.cntrlr.getBButton() == True:
            self.wrist.set(0.3)
        else:
            self.wrist.set(0)

        if self.cntrlr.getTriggerAxis(0) > 0.05:
            self.Lintake.set(0.7)
        elif self.cntrlr.getTriggerAxis(1) > 0.05:
            self.Lintake.set(-0.7)
        else:
            self.Lintake.set(0)

        motorOutput = self.Lift1.getMotorOutputPercent()

        sb = []
        sb.append("\tOut%%: %.3f" % motorOutput)
        sb.append("\tVel: %.3f" % self.Lift1.getSelectedSensorVelocity(self.kPIDLoopIdx))

        self.processInstrumentation(self.Lift1 , sb)

    def processInstrumentation(self, tal, sb):

        # smart dash plots
        wpilib.SmartDashboard.putNumber("SensorVel", tal.getSelectedSensorVelocity(self.kPIDLoopIdx))
        wpilib.SmartDashboard.putNumber("SensorPos", tal.getSelectedSensorPosition(self.kPIDLoopIdx))
        wpilib.SmartDashboard.putNumber("MotorOutputPercent", tal.getMotorOutputPercent())
        wpilib.SmartDashboard.putNumber("ClosedLoopError", tal.getClosedLoopError(self.kPIDLoopIdx))

        # check if we are motion-magic-ing
        if tal.getControlMode() == ctre.WPI_TalonSRX.ControlMode.MotionMagic:
            self.timesInMotionMagic += 1
        else:
            self.timesInMotionMagic = 0

        if self.timesInMotionMagic > 10:
            # print the Active Trajectory Point Motion Magic is servoing towards
            wpilib.SmartDashboard.putNumber("ClosedLoopTarget", tal.getClosedLoopTarget(self.kPIDLoopIdx))

            if not self.isSimulation():
                wpilib.SmartDashboard.putNumber("ActTrajVelocity", tal.getActiveTrajectoryVelocity())
                wpilib.SmartDashboard.putNumber("ActTrajPosition", tal.getActiveTrajectoryPosition())
                wpilib.SmartDashboard.putNumber("ActTrajHeading", tal.getActiveTrajectoryHeading())

        # periodically print to console
        self.loops += 1
        if self.loops >= 10:
            self.loops = 0
            print(' '.join(sb))

if __name__ == '__main__':
    wpilib.run(MyRobot)
