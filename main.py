#!/usr/bin/env python3

# OUTPUT_A - prawy motor
# OUTPUT_B - lewy motor
# INPUT_2 - prawy sensor
# INPUT_3 - lewy sensor

from time import sleep
import ev3dev.ev3 as ev3
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank

color_dict = {
        0: 'No color',
        1: 'Black',
        2: 'Blue',
        3: 'Green',
        4: 'Yellow',
        5: 'Red',
        6: 'White',
        7: 'Brown',
}



# ts = ev3.TouchSensor()
# m = LargeMotor('outA')
# m.on_for_rotations(SpeedPercent(75), 5)
# m = ev3.LargeMotor('outA')
# m.run_timed(time_sp=3000, speed_sp=500)
# while True:
#     ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])
tank_drive = MoveTank('outA', 'outD')

# # drive in a turn for 5 rotations of the outer motor
# # the first two parameters can be unit classes or percentages.
# tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(75), 10)

# # drive in a different turn for 3 seconds
# tank_drive.on_for_seconds(SpeedPercent(60), SpeedPercent(30), 3)


right_motor = LargeMotor(OUTPUT_A)
left_motor = LargeMotor(OUTPUT_D)

# m.on_for_rotations(SpeedPercent(20), 10)

# tank_drive.on_for_seconds(SpeedPercent(20), SpeedPercent(20), 10)

right_sensor = ColorSensor(INPUT_2)
left_sensor = ColorSensor(INPUT_3)
i = 0

# 2 białe - prosto
# jak prawy będzie czarny i lewy biały -> skręć w prawo
speed_straigt = 25
speed_turn = 15

state_dict = {
    0: 'prosto',
    1: 'prawo',
    2: 'lewo'
}

turning_time = 0
TURN_THRESHOLD = 5
last_state = 0

while True:
    if right_sensor.color != 6 and left_sensor.color == 6:
        while True:
            # sleep(0.5)
            last_state = 1
            print("skrecam w prawo")
            # skręt w prawo
            # right_motor.stop()
            right_motor.on(SpeedPercent(-speed_turn//2))
            left_motor.on(SpeedPercent(speed_turn))
            if right_sensor.color == 6 and left_sensor.color == 6:
                break
    elif right_sensor.color == 6 and left_sensor.color != 6:
        while True:
            # sleep(0.5)
            last_state = 2
            print("skrecam w lewo")
            # left_motor.stop()
            left_motor.on(SpeedPercent(-speed_turn//2))
            right_motor.on(SpeedPercent(speed_turn))
            if right_sensor.color == 6 and left_sensor.color == 6:
                break
    # elif right_sensor.color != 6 and left_sensor.color != 6:
    #     # rób to co ostatnio
    #     if last_state == 0:
    #         right_motor.on(SpeedPercent(speed_straigt))
    #         left_motor.on(SpeedPercent(speed_straigt))
    #     elif last_state == 1:
    #         right_motor.on(SpeedPercent(-speed_turn))
    #         left_motor.on(SpeedPercent(speed_turn))
    #     else:
    #         left_motor.on(SpeedPercent(-speed_turn))
    #         right_motor.on(SpeedPercent(speed_turn))
    else:
        print("jade prosto")
        # if turning_time < TURN_THRESHOLD:
            # lekki skręt, jedźmy normalnie prosto

        right_motor.on(SpeedPercent(speed_straigt))
        left_motor.on(SpeedPercent(speed_straigt))
        # else:
            # mocny skręt, trzeba dokręcić :)
        # print("zatrzymuje sie :)")
        # right_motor.stop()
        # left_motor.stop()

    sleep(0.1)
    print("prawy kolor: {}".format(color_dict[right_sensor.color]))
    print("lewy kolor: {}".format(color_dict[left_sensor.color]))
    i += 1


