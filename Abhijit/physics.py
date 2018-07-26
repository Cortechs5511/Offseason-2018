import math

from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import sim.simComms as simComms

class PhysicsEngine(object):
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.position = 0

        # Change these parameters to fit your robot!
        bumper_width = 3.5*units.inch

        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
            120*units.lbs,                      # robot mass
            10.71,                              # drivetrain gear ratio
            3,                                  # motors per side
            30*units.inch,                      # robot wheelbase
            32*units.inch + bumper_width*2,     # robot width
            32*units.inch + bumper_width*2,     # robot length
            4*units.inch                        # wheel diameter
        )

        # Precompute the encoder constant
        # -> encoder counts per revolution / wheel circumference
        self.kEncoder = 360 / (0.5 * math.pi)

        self.l_distance = 0
        self.r_distance = 0

    def update_sim(self, hal_data, now, tm_diff):
        # Simulate the drivetrain
        l_motor = hal_data['CAN'][10]['value']
        r_motor = hal_data['CAN'][20]['value']

        x, y, angle = self.drivetrain.get_distance(l_motor, r_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)

        # Update encoders
        #print(simComms.getEncoders())
        if(simComms.getEncoders()==True):
            self.l_distance = 0
            self.r_distance = 0
            simComms.resetEncodersSim()
        else:
            self.l_distance += self.drivetrain.l_velocity * tm_diff
            self.r_distance += self.drivetrain.r_velocity * tm_diff

        hal_data['encoder'][0]['count'] = int(self.l_distance * self.kEncoder)
        hal_data['encoder'][1]['count'] = int(self.r_distance * self.kEncoder)
