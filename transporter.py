#!/usr/bin/env python3
import ev3dev.ev3 as ev3 
from ev3dev2.motor import MoveTank, MediumMotor
from ev3dev2.sensor.lego import TouchSensor
from time import sleep

def scale(readings):
    return (int(100 * readings[0] / 66), int(100 * readings[1] / 90))

def minmax(val):
    if val <= -100:
        return -100
    elif val >= 100:
        return 100
    else: return val

s1 = ev3.ColorSensor('in1')
s2 = ev3.ColorSensor('in3')
#butt = TouchSensor('in3')
tank = MoveTank('outA', 'outD')
# lever = MediumMotor('outC')
payload_detected = False
backing_with_payload = False
on_entry = False 
double_trouble = 0
w_payload = False 

while True:
    reading = scale((s1.reflected_light_intensity, s2.reflected_light_intensity))
    error = reading[0] - reading[1]
    tank.on(minmax(20 + 0.5 * error), minmax(20 - 0.5 * error))
    col1 = s1.color
    col2 = s2.color

    if double_trouble > 3:
        double_trouble = 0 
        on_entry = False
    

    # payload approach state
    if col1 == 5 and col2 == 5:
        double_trouble += 1
        if not on_entry and not backing_with_payload:
            tank.off()
            sleep(0.5)
            # back off
            tank.on_for_rotations(-50, -50, 2)
            # turn
            tank.on_for_rotations(-30, 30, 2.9)
            # back up
            tank.on_for_rotations(-50, -50, 2.3)
            # pick up
            # lever.on_for_rotations(30, 4)
            tank.on_for_rotations(-50, -50, 0.8)
            # exit state
            backing_with_payload = True 
            w_payload = True

    # entering approching trajectory state
    elif col1 == 5 and not backing_with_payload and not on_entry and not w_payload:
        tank.off()
        tank.on_for_rotations(20, 20, 1)
        tank.on_for_rotations(-30, 30, 1.5)
        #tank.on_for_rotations(100, 100, 1)
        on_entry = True
    elif col2 == 5 and not backing_with_payload and not on_entry and not w_payload:
        tank.off()
        tank.on_for_rotations(20, 20, 1)
        tank.on_for_rotations(30, -30, 1.5)
        #tank.on_for_rotations(100, 100, 1)
        on_entry = True
    # going back on track 
    elif backing_with_payload and col1 == 1:
        tank.on_for_rotations(30, 30, 1)
        tank.on_for_rotations(-30, 30, 1.3)
        backing_with_payload = False 

    elif backing_with_payload and col2 == 1:
        tank.on_for_rotations(30, 30, 1)
        tank.on_for_rotations(-30, 30, 1.3)
        backing_with_payload = False 

   # elif col1 == 2 and col2 == 2:
   #     double_trouble += 1
   #     if not on_entry and not backing_with_payload:
   #         tank.off()
   #         sleep(0.5)
   #         # back off
   #         tank.on_for_rotations(-50, -50, 2)
   #         # turn
   #         tank.on_for_rotations(-30, 30, 2.9)
   #         # back up
   #         tank.on_for_rotations(-50, -50, 2.3)
   #         # pick up
   #         lever.on_for_rotations(-30, 4)
   #         tank.on_for_rotations(-50, -50, 0.8)
   #         # exit state
   #         backing_with_payload = True 
   #         w_payload = False
#
   # elif w_payload and col1 and not on_entry = 2:
   #     tank.off()
   #     tank.on_for_rotations(20, 20, 1)
   #     tank.on_for_rotations(-30, 30, 1.5)
   #     on_entry = True
#
   # elif w_payload and col2 and not on_entry = 2:
   #     tank.off()
   #     tank.on_for_rotations(20, 20, 1)
   #     tank.on_for_rotations(30, -30, 1.5)
   #     on_entry = True
#

    