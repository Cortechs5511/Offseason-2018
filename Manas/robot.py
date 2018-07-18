import wpilib
import wpilib.drive
import ctre
#Manas Takalpati

class Robot5511(wpilib.IterativeRobot):

    def robotInit(self):
        #drive portion
        self.left_motor1 = ctre.WPI_TalonSRX(7)
        self.left_motor2 = ctre.WPI_VictorSPX(8)
        self.left_motor3 = ctre.WPI_VictorSPX(9)
        self.left_side = wpilib.SpeedControllerGroup(self.left_motor1, self.left_motor2, self.left_motor3)

        self.right_motor1 = ctre.WPI_TalonSRX(17)
        self.right_motor2 = ctre.WPI_VictorSPX(18)
        self.right_motor3 = ctre.WPI_VictorSPX(19)
        self.right_side = wpilib.SpeedControllerGroup(self.right_motor1, self.right_motor2, self.right_motor3)

        self.drive = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)
        self.drive.setExpiration(0.1)
        self.stick_left = wpilib.Joystick(0)
        self.stick_right = wpilib.Joystick(1)


        #encoders


        #timer
        self.timer = wpilib.Timer()

        #operator, arbitrary motor controllers and ports for now
        self.lift_motor = ctre.WPI_VictorSPX(3)
        self.intake_motor_left = ctre.WPI_VictorSPX(4)
        self.intake_motor_right = ctre.WPI_VictorSPX(5)
        self.intake = wpilib.SpeedControllerGroup(self.intake_motor_left, self.intake_motor_right)
        self.xbx = wpilib.XboxController(2)

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        if self.timer.get() < 6.0:
            self.drive.tankDrive(.7, -.7)
        else:
            self.drive.tankDrive(0, 0)

    def teleopInit(self):
        self.timer.reset()

    def teleopPeriodic(self):
        self.drive.setDeadband(.1)
        self.drive.tankDrive(self.stick_left.getY(), self.stick_right.getY() * -1)

        #if right hand analog stick is moved (1 is right hand, or kRight based on what I saw in the GenericHID source code), then lift based on X axis value
        if (self.xbx.getTriggerAxis(1) > 0):
            self.lift_motor.set(.6)
        elif (self.xbx.getTriggerAxis(1) < 0):
            self.lift_motor.set(.6)
        else:
            pass

        #if A button pressed, set intake speed to 80%
        if (self.xbx.getAButton() ==  True):
            self.intake.set(.8)
        else:
            pass

if __name__ == '__main__':
    wpilib.run(Robot5511, physics_enabled=True)