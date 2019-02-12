#!/usr/bin/env python3

import ev3.ev3motor as ev3
import importlib
import datetime
from ev3.sensorcar import *

car = SensorCar() 


movequeue = []
# queueitem = ev3.QueueItem(startaction = car.go, startkwargs = {"speed": 500, "seconds": 4, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.sound.beep, startkwargs = {"args": "-f 300.7 -r 2 -d 100 -l 400"}, runtime = 1)
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.go, startkwargs = {"speed": -500, "seconds": 3, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.tightTurn, startkwargs = {"direction": "left", "degrees": 180, "speed": 300, "wait": False, "gyro": car.gyro})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.go, startkwargs = {"speed": 500, "inches": 10, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.go, startkwargs = {"speed": 500, "inches": -10, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.go, startkwargs = {"inches": 5, "seconds": 1, "wait": False})
# movequeue.append(queueitem)
# queueitem = ev3.QueueItem(startaction = car.go, startkwargs = {"inches": -5, "seconds": 1, "wait": False})
# movequeue.append(queueitem)

queueitem = ev3.QueueItem(startaction = car.tightTurn, startkwargs = {"direction": "left", "degrees": 180, "speed": 10, "wait": False, "gyro": car.gyro}, runtime = 3)
movequeue.append(queueitem)
queueitem = ev3.QueueItem(startaction = car.Stop, runtime = 3)
movequeue.append(queueitem)


activeitem = False
while True:
  print(car.gyro.angle)
  if not activeitem or datetime.datetime.now() >= activeitem.stoptime:
    if activeitem and activeitem.stopaction:
      if activeitem.stopkwargs:
        activeitem.stopaction(**activeitem.stopkwargs)
      else:
        activeitem.stopaction()

    if len(movequeue) > 0:
      activeitem = movequeue.pop(0)
      if activeitem.startkwargs:
        activeitem.stoptime = activeitem.startaction(**activeitem.startkwargs)
      else:
        activeitem.stoptime = activeitem.startaction()
      
      if activeitem.runtime:
        activeitem.stoptime = datetime.datetime.now() + datetime.timedelta(seconds = activeitem.runtime)
      elif not active.stoptime:
        active.stoptime = datetime.datetime.now()

  if car.touch.is_pressed:
    car.sound.beep()

  if car.color.color == 2:
    car.sound.play_song((
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

