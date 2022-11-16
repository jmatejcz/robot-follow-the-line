#!/usr/bin/env python3

# OUTPUT_A - prawy motor
# OUTPUT_B - lewy motor
# INPUT_2 - prawy sensor
# INPUT_3 - lewy sensor

from time import sleep
import ev3dev.ev3 as ev3
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_1
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_C,OUTPUT_B, SpeedPercent, MoveTank, MediumMotor

motor_crane = MediumMotor(OUTPUT_D)
sensor_eyes = InfraredSensor(INPUT_2)
#minus to do góry

# # m.run_forever()

# while 1>0:
# # sleep(0.5)
#     print("Distance: {}".format(sensor_eyes.proximity))     
# # motor_crane.on(SpeedPercent(-30))
# # # sleep(3)
# # motor_crane.on_for_rotations(SpeedPercent(15), 4)
# # sleep(3)
# # motor_crane.on_for_rotations(SpeedPercent(-15), 2)



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


BLACKS = ['Black','Brown', 'Red']
YELLOWS = ['Yellow', 'Green']
RED = ['Red']
GREEN = ['Green']
BLUE = ['Blue']



right_motor = LargeMotor(OUTPUT_A)
left_motor = LargeMotor(OUTPUT_C)

right_sensor = ColorSensor(INPUT_3)
left_sensor = ColorSensor(INPUT_1)

COLOR_DETECT_COUNTER = 0

i = 0

# 2 białe - prosto
# jak prawy będzie czarny i lewy biały -> skręć w prawo

# wolne w maire dziala
speed_straigt = 15
speed_turn = 15
# SLEEP_TIME = 0.15
ROT_90 = 1

# speed_straigt = 25
# speed_turn = 15

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
    # print("prawy kolor: {}".format(color_value_name_dict[r_color]))
    # print("lewy kolor: {}".format(color_value_name_dict[l_color]))
    print("prawy kolor: {}".format(r_color))
    print("lewy kolor: {}".format(l_color))


def turn_180():
    left_motor.on_for_rotations(SpeedPercent(-speed_turn), 2*ROT_90)
    right_motor.on_for_rotations(SpeedPercent(speed_turn), 2*ROT_90)


while True:
    try:
        left_color = color_value_name_dict[left_sensor.color]
        right_color = color_value_name_dict[right_sensor.color]
        if right_color in BLACKS and left_color == 'White':
            if right_color == 'Red':
                COLOR_DETECT_COUNTER += 1

            while True:
                print_colors(right_color, left_color)
                print("skrecam w prawo")

                right_motor.on(SpeedPercent(-speed_turn))
                left_motor.on(SpeedPercent(speed_turn))

                # sleep(SLEEP_TIME)
                left_color = color_value_name_dict[left_sensor.color]
                right_color = color_value_name_dict[right_sensor.color]
                

                print_colors(right_color, left_color)

                if right_color == 'White' and left_color == 'White':
                    break

                # zapobiega wyjściu na skrzyżowaniu
                if right_color in BLACKS and left_color in BLACKS:
                    break

        # skręt w lewo
        elif right_color == 'White' and left_color in BLACKS:
            if left_color == 'Red':
                COLOR_DETECT_COUNTER += 1

            while True:
                
                
                print_colors(right_color, left_color)
                print("skrecam w lewo")

                left_motor.on(SpeedPercent(-speed_turn))
                right_motor.on(SpeedPercent(speed_turn))

                # sleep(SLEEP_TIME)
                left_color = color_value_name_dict[left_sensor.color]
                right_color = color_value_name_dict[right_sensor.color]

                print_colors(right_color, left_color)

                if right_color == 'White' and left_color == 'White':
                    break
                if right_color in BLACKS and left_color in BLACKS:
                    break

        # czerowny po prawej
        # elif right_color in RED:
        #     print_colors(right_color, left_color)
        #     print("obkrecam 90 stopni bo widze czerwony")
        #     left_motor.on_for_rotations(SpeedPercent(-speed_turn), ROT_90)
        #     right_motor.on_for_rotations(SpeedPercent(speed_turn), ROT_90)

        #     # cofam 
        #     while sensor_eyes.proximity > 25:
        #         print("Distance: {}".format(sensor_eyes.proximity))
        #         left_motor.on(SpeedPercent(-speed_straigt))
        #         right_motor.on(SpeedPercent(-speed_straigt))

        #     print("podnosze dzwig i ide spanko")
        #     left_motor.on(SpeedPercent(0))
        #     right_motor.on(SpeedPercent(0))
        #     sleep(2.0)


        # elif right_color == 'Red' and left_color == 'Red':
        #     turn_180()
        #     # jedziemy w tył while odległość > ileś
        #     # cofam 
        #     while sensor_eyes.proximity > 30:
        #         print("Distance: {}".format(sensor_eyes.proximity))
        #         left_motor.on(SpeedPercent(-speed_straigt))
        #         right_motor.on(SpeedPercent(-speed_straigt))

        #     # koniec cofki - podnosimy
        #     motor_crane.on_for_rotations(SpeedPercent(-15), 4)
    
        #     # podniśliśmy
        #     # jedź prosto dopóki nie są 2 czerwone
        #     while right_color == 'Red' and left_color == 'Red':
        #         left_color = color_value_name_dict[left_sensor.color]
        #         right_color = color_value_name_dict[right_sensor.color]

        #         left_motor.on(SpeedPercent(speed_straigt))
        #         right_motor.on(SpeedPercent(speed_straigt))

        # # zolty po prawej
        # elif right_color in YELLOWS:
        #     print_colors(right_color, left_color)
        #     left_motor.on_for_rotations(SpeedPercent(-speed_turn), ROT_90)
        #     right_motor.on_for_rotations(SpeedPercent(speed_turn), ROT_90)

        # # zielony po prawej
        # elif right_color in GREEN:
        #     print_colors(right_color, left_color)
        #     left_motor.on_for_rotations(SpeedPercent(-speed_turn), ROT_90)
        #     right_motor.on_for_rotations(SpeedPercent(speed_turn), ROT_90)
        else:
            print_colors(right_color, left_color)
            print("jade prosto")

            right_motor.on(SpeedPercent(speed_straigt))
            left_motor.on(SpeedPercent(speed_straigt))

        # sleep(0.1)




    except Exception as e:
        continue


