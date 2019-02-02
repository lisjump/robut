#!/usr/bin/env python3

import ev3.ev3motor as ev3
import importlib

left = ev3.MyMotor(port = "B", tireradius = .73)
right = ev3.MyMotor(port = "C", tireradius = .73)
car = ev3.TankCar(left=left, right=right)
car.goStraight(speed=500, seconds=3)
car.goStraight(speed=-500, seconds=3)
car.goStraight(speed=500, inches=10)
car.goStraight(speed=500, inches=-10)
car.goStraight(inches=10, seconds=1.569)
car.goStraight(inches=-10, seconds=1.569)

# comment