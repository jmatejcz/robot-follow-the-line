#!/usr/bin/env python3

# OUTPUT_A - prawy motor
# OUTPUT_B - lewy motor
# INPUT_2 - prawy sensor
# INPUT_3 - lewy sensor

from time import sleep
import ev3dev.ev3 as ev3
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_1
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor

# motor_crane = MediumMotor(OUTPUT_C)
# sensor_eyes = InfraredSensor(INPUT_2)


# # m.run_forever()

# while True:
#     sleep(0.5)
#     print("Distance: {}".format(sensor_eyes.proximity))
#     # motor_crane.on(SpeedPercent(5))




color_value_name_dict = {
        0: 'No color',
        1: 'Black',
        2: 'Blue',
        3: 'Green',
        4: 'Yellow',
        5: 'Red',
        6: 'White',
        7: 'Brown',
}

color_name_value_dict = {
    'No color': 0,
    'Black': 1,
    'Blue': 2,
    'Green': 3,
    'Yellow': 4,
    'Red': 5,
    'White': 6,
    'Brown': 7
}


BLACKS = [1, 7]
YELLOWS = [4]



right_motor = LargeMotor(OUTPUT_A)
left_motor = LargeMotor(OUTPUT_D)

right_sensor = ColorSensor(INPUT_3)
left_sensor = ColorSensor(INPUT_1)
i = 0

# 2 białe - prosto
# jak prawy będzie czarny i lewy biały -> skręć w prawo
speed_straigt = 40
speed_turn = 20

state_dict = {
    0: 'prosto',
    1: 'prawo',
    2: 'lewo'
}

# zólty = blue
# blue = blue
# red = red
# green = green

def print_colors(r_color, l_color):
    print("prawy kolor: {}".format(color_value_name_dict[r_color]))
    print("lewy kolor: {}".format(color_value_name_dict[l_color]))


while True:
    try:
        if right_sensor.color in BLACKS and color_value_name_dict[left_sensor.color] == 'White':
            while True:
                # sleep(0.2)
                print("skrecam w prawo")
                print_colors(right_sensor.color, left_sensor.color)

                right_motor.on(SpeedPercent(-speed_turn//2))
                left_motor.on(SpeedPercent(speed_turn))
                if color_value_name_dict[right_sensor.color] == 'White' and color_value_name_dict[left_sensor.color] == 'White':
                    break
                if right_sensor.color in BLACKS and left_sensor.color in BLACKS:
                    break
        elif color_value_name_dict[right_sensor.color] == 'White' and left_sensor.color in BLACKS:
            while True:
                # sleep(0.2)
                
                print("skrecam w lewo")
                print_colors(right_sensor.color, left_sensor.color)

                left_motor.on(SpeedPercent(-speed_turn//2))
                right_motor.on(SpeedPercent(speed_turn))
                if color_value_name_dict[right_sensor.color] == 'White' and color_value_name_dict[left_sensor.color] == 'White':
                    break
                if right_sensor.color in BLACKS and left_sensor.color in BLACKS:
                    break

        else:
            print("jade prosto")
            print_colors(right_sensor.color, left_sensor.color)

            right_motor.on(SpeedPercent(speed_straigt))
            left_motor.on(SpeedPercent(speed_straigt))
        sleep(0.1)


    except (OSError, ValueError) as e:
        continue


