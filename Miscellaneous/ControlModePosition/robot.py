import wpilib
import ctre

class Robot5511(wpilib.IterativeRobot):

    def robotInit(self):
        self.posmotor = ctre.WPI_TalonSRX(40)

        self.posmotor.set(ctre.WPI_TalonSRX.ControlMode.Position)

        self.PIDp = 1
        self.PIDi = 0
        self.PIDd = 0
        self.input = self.posmotor
        self.output = wpilib.interfaces.PIDOutput()

        self.robotPID = wpilib.PIDController(self.PIDp, self.PIDi, self.PIDd, self.input, self.output)

    def robotPeriodic(self):

    def autonomousInit(self):

    def autonomousPeriodic(self):

    def teleopInit(self):

    def teleopPeriodic(self):
        self.posmotor.set(1)


if __name__ == 'main':
    wpilib.run(Robot5511, physics_enabled=True)
