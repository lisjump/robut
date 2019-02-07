#!/usr/bin/env python3

import ev3.ev3motor as ev3
import importlib
import datetime

left = ev3.MyMotor(port = "B", tireradius = .73)
right = ev3.MyMotor(port = "C", tireradius = .73)
car = ev3.TankCar(left=left, right=right, axlelength=3.9)
movequeue = []
queueitem = ev3.QueueItem(startaction = car.goStraight, startkwargs = {"speed": 500, "seconds": 3, "wait": False})
movequeue.append(queueitem)
queueitem = ev3.QueueItem(startaction = car.goStraight, startkwargs = {"speed": -500, "seconds": 3, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.goStraight, startkwargs = {"speed": 500, "inches": 10, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.goStraight, startkwargs = {"speed": 500, "inches": -10, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.goStraight, startkwargs = {"inches": 5, "seconds": 1, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.goStraight, startkwargs = {"inches": -5, "seconds": 1, "wait": False})
# movequeue.append(queueitem)

touch = ev3.TouchSensor()
sound = ev3.Sound()
color = ev3.ColorSensor()
gyro = ev3.GyroSensor()



activeitem = False
while True:
  if not activeitem or datetime.datetime.now() >= activeitem.stoptime:
    if activeitem and activeitem.stopaction:
      activeitem.stopaction(**activeitem.stopkwargs)
    if len(movequeue) > 0:
      activeitem = movequeue.pop(0)
      activeitem.stoptime = activeitem.startaction(**activeitem.startkwargs)
      if activeitem.runtime:
          activeitem.stoptime = datetime.datetime.now() + timedelta("seconds = " + command[4])

  if touch.is_pressed:
    sound.play_song((
      ('D4', 'e3'),
      ('D4', 'e3'),
      ('D4', 'e3'),
      ('G4', 'h'),
      ('D5', 'h')
    ))


  if color.color == 1:
    sound.play_song((
      ('D4', 'e3'),      # intro anacrouse
      ('D4', 'e3'),
      ('D4', 'e3'),
      ('G4', 'h'),       # meas 1
      ('D5', 'h'),
      ('C5', 'e3'),      # meas 2
      ('B4', 'e3'),
      ('A4', 'e3'),
      ('G5', 'h'),
      ('D5', 'q'),
      ('C5', 'e3'),      # meas 3
      ('B4', 'e3'),
      ('A4', 'e3'),
      ('G5', 'h'),
      ('D5', 'q'),
      ('C5', 'e3'),      # meas 4
      ('B4', 'e3'),
      ('C5', 'e3'),
      ('A4', 'h.'),
    ))
