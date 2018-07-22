import wpilib
import wpilib.drive
import ctre
#Manas Takalpati

class Robot5511(wpilib.IterativeRobot):

    def robotInit(self):
        #drive portion
        self.Tleft = ctre.WPI_TalonSRX(10)
        self.Vleft1 = ctre.WPI_VictorSPX(11)
        self.Vleft2 = ctre.WPI_VictorSPX(12)
        self.Vleft1.set(ctre.WPI_VictorSPX.ControlMode.Follower, 10)
        self.Vleft2.set(ctre.WPI_VictorSPX.ControlMode.Follower, 10)

        self.Tright = ctre.WPI_TalonSRX(20)
        self.Vright1 = ctre.WPI_VictorSPX(21)
        self.Vright2 = ctre.WPI_VictorSPX(22)
        self.Vright1.set(ctre.WPI_VictorSPX.ControlMode.Follower, 20)
        self.Vright2.set(ctre.WPI_VictorSPX.ControlMode.Follower, 20)

        self.drive = wpilib.drive.DifferentialDrive(self.Tleft, self.Tright)
        self.drive.setExpiration(0.1)
        self.stick_left = wpilib.Joystick(0)
        self.stick_right = wpilib.Joystick(1)


        #encoders


        #timer
        self.timer = wpilib.Timer()

        #operator
        self.liftMain = ctre.WPI_TalonSRX(30)
        self.lift2 = ctre.WPI_TalonSRX(31)
        self.lift2.set(ctre.WPI_TalonSRX.ControlMode.Follower, 30)

        self.wrist = ctre.WPI_TalonSRX(40)

        self.intakeLeft = ctre.WPI_TalonSRX(50)
        self.intakeRight = ctre.WPI_TalonSRX(51)
        self.intakeRight.set(ctre.WPI_TalonSRX.ControlMode.Follower, 50)

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
            self.lift_motor.set(-.6)
        else:
            pass

        #if A button pressed, set intake speed to 80%
        if (self.xbx.getAButton() ==  True):
            self.intakeLeft.set(.8)
        else:
            pass

        #if left hand analog stick moved up then wrist forward, else if moved down, wrist backward
        if (self.xbx.getTriggerAxis(0) > 0):
            self.lift_motor.set(.6)
        elif (self.xbx.getTriggerAxis(0) < 0):
            self.lift_motor.set(-.6)
        else:
            pass

if __name__ == '__main__':
    wpilib.run(Robot5511, physics_enabled=True)