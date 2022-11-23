#!/usr/bin/env python3

from time import sleep
import ev3dev.ev3 as ev3
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_1
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_C,OUTPUT_B, SpeedPercent, MoveTank, MediumMotor

motor_crane = MediumMotor(OUTPUT_B)
sensor_eyes = InfraredSensor(INPUT_3)

right_motor = LargeMotor(OUTPUT_A)
left_motor = LargeMotor(OUTPUT_D)

right_sensor = ColorSensor(INPUT_1)
left_sensor = ColorSensor(INPUT_2)

# czerwony = (200,7,10)
# blue = (11, 50, 160)
# żółty = (255, 200, 50)
# zielony = (10, 70,50)
# biały = (255, 220, 255)
# czarny = (5, 5, 10)

def get_color(sensor):
    r, g, b = sensor.rgb
    if r > 150 and g < 40 and b < 40:
        return 'Red'
    elif r < 50 and g < 80 and b > 120:
        return 'Blue'
    elif r > 150 and g > 120:
        if b < 80:
            return 'Yellow'
        else:
            return 'White'
    elif r < 30 and g < 30 and b < 30:
        return 'Black'
    
    return 'ERROR'

speed_straigt = 25
speed_turn = 15
ROT_90 = 1
TURN = ''
ROT_TIME = 2.5
BLACKS = ['Black']
ITEM = False
CRANE_ROTATIONS=5

def print_colors(r_color, l_color):
    print("prawy kolor: {}".format(r_color))
    print("lewy kolor: {}".format(l_color))


def turn_180():
    left_motor.on(SpeedPercent(-speed_turn))
    right_motor.on(SpeedPercent(speed_turn))


while True:
    try:
        left_color = get_color(left_sensor)
        right_color = get_color(right_sensor)
        print('left: {}'.format(left_sensor.rgb))
        print('right: {}'.format(right_sensor.rgb))
        if right_color in BLACKS and left_color == 'White':
            while True:
                print_colors(right_color, left_color)
                print("skrecam w prawo")

                right_motor.on(SpeedPercent(-speed_turn))
                left_motor.on(SpeedPercent(speed_turn))

                left_color = get_color(left_sensor)
                right_color = get_color(right_sensor)
                print_colors(right_color, left_color)

                if right_color == 'White' and left_color == 'White':
                    break

                # zapobiega wyjściu na skrzyżowaniu
                if right_color == 'Black' and left_color == 'Black':
                    break

        # skręt w lewo
        elif right_color == 'White' and left_color in BLACKS:
            while True:
                print_colors(right_color, left_color)
                print("skrecam w lewo")

                left_motor.on(SpeedPercent(-speed_turn))
                right_motor.on(SpeedPercent(speed_turn))

                left_color = get_color(left_sensor)
                right_color = get_color(right_sensor)

                print_colors(right_color, left_color)

                if right_color == 'White' and left_color == 'White':
                    break
                if right_color == 'Black' and left_color == 'Black':
                    break

        # wjechaliśmy na pole koloru
        elif right_color in ['Red', 'Yellow', 'Blue'] and left_color in ['Red', 'Yellow', 'Blue']:
            left_color = get_color(left_sensor)
            right_color = get_color(right_sensor)

            right_motor.on(SpeedPercent(-speed_turn))
            left_motor.on(SpeedPercent(-speed_turn))
            sleep(3)

            if not ITEM:
                while sensor_eyes.proximity > 30:
                    turn_180()
                    sleep(0.5)
                    print("Distance: {}".format(sensor_eyes.proximity))

                while sensor_eyes.proximity > 13:
                    right_motor.on(SpeedPercent(-speed_turn))
                    left_motor.on(SpeedPercent(-speed_turn))
                    print("cofka Distance: {}".format(sensor_eyes.proximity))

                left_motor.on(SpeedPercent(0))
                right_motor.on(SpeedPercent(0))
                motor_crane.on_for_rotations(SpeedPercent(-20), CRANE_ROTATIONS)
                ITEM = True
            else:
                turn_180()
                sleep(5)
                left_motor.on(SpeedPercent(0))
                right_motor.on(SpeedPercent(0))
                motor_crane.on_for_rotations(SpeedPercent(20), CRANE_ROTATIONS)
                ITEM = False
    
            while right_color == get_color(right_sensor) and left_color == get_color(left_sensor):
                left_color = get_color(left_sensor)
                right_color = get_color(right_sensor)

                left_motor.on(SpeedPercent(speed_straigt))
                right_motor.on(SpeedPercent(speed_straigt))

        elif right_color in ['Red', 'Yellow', 'Blue'] and left_color == 'White' and TURN == '':
            print_colors(right_color, left_color)
            right_motor.on(SpeedPercent(-speed_turn))
            left_motor.on(SpeedPercent(speed_turn))
            sleep(ROT_TIME)

            TURN = 'RIGHT'

        
        elif left_color in ['Red', 'Yellow', 'Blue'] and right_color == 'White' and TURN == '':
            print_colors(right_color, left_color)
            right_motor.on(SpeedPercent(speed_turn))
            left_motor.on(SpeedPercent(-speed_turn))
            sleep(ROT_TIME)
            TURN = 'LEFT'

        elif left_color in BLACKS and right_color in ['Red', 'Yellow', 'Blue'] or right_color in BLACKS and left_color in ['Red', 'Yellow', 'Blue'] and TURN:
            if TURN == 'LEFT':
                print("WYJEZDZAM Z DOJAZDU DO POLA")
                left_motor.on_for_rotations(SpeedPercent(-speed_turn), ROT_90)
                right_motor.on_for_rotations(SpeedPercent(speed_turn), ROT_90)
                TURN = ''
            else:
                print("WYJEZDZAM Z DOJAZDU DO POLA")
                left_motor.on_for_rotations(SpeedPercent(speed_turn), ROT_90)
                right_motor.on_for_rotations(SpeedPercent(-speed_turn), ROT_90)
                TURN = ''


        else:
            print_colors(right_color, left_color)
            print("jade prosto")

            if right_color == 'Black' and left_color == 'Black' and TURN == 'LEFT':
                print("WYJEZDZAM Z DOJAZDU DO POLA")
                left_motor.on_for_rotations(SpeedPercent(-speed_turn), ROT_90)
                right_motor.on_for_rotations(SpeedPercent(speed_turn), ROT_90)
                TURN = ''
            elif right_color == 'Black' and left_color == 'Black' and TURN == 'RIGHT':
                print("WYJEZDZAM Z DOJAZDU DO POLA")
                left_motor.on_for_rotations(SpeedPercent(speed_turn), ROT_90)
                right_motor.on_for_rotations(SpeedPercent(-speed_turn), ROT_90)
                TURN = ''

            right_motor.on(SpeedPercent(speed_straigt))
            left_motor.on(SpeedPercent(speed_straigt))

    except Exception as e:
        continue
