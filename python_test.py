#!/usr/bin/env python3
from math import degrees
import ev3dev.ev3 as ev3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds


from ev3dev2.sensor.lego import GyroSensor

# Instantiate the MoveTank object
# tank = MoveTank(OUTPUT_A, OUTPUT_B)

# # Initialize the tank's gyro sensor
# tank.gyro = GyroSensor()

# # Calibrate the gyro to eliminate drift, and to initialize the current angle as 0
# tank.gyro.calibrate()

# # Pivot 30 degrees
# tank.turn_degrees(
#     speed=SpeedPercent(5),
#     target_angle=30
# )

# ts = ev3.TouchSensor()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
# # drive in a turn for 10 rotations of the outer motor
tank_drive.on_for_rotations(20, 0, 10)
# tank_drive.turn_right(
#     speed=SpeedPercent(5),
#     degrees=30
# )

# m = ev3.LargeMotor('outA')
# m.run_timed(time_sp=3000, speed_sp=500)
# while True:
#     ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])

