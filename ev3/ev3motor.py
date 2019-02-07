#!/usr/bin/env python3
from ev3dev.ev3 import *
import math 
import datetime 

class QueueItem():
  def __init__(self, startaction, startkwargs = None, stopaction = None, stopkwargs = None, runtime = None):
    self.startaction = startaction
    self.startkwargs = startkwargs
    self.stopaction = stopaction
    self.stopkwargs = startkwargs
    self.runtime = runtime
    self.stoptime = None

class Queue():
  def __init__(self):
    self.queue = []

class MyMotor(Motor):
  def __init__(self, port, reversed = 0, tireradius = None, defaultSpeed = 0):
    if port.upper() not in ["A", "B", "C", "D"]:
      print("Error: Port must be A, B, C, or D")
      return
    Motor.__init__(self, 'out' + port.upper())
    if reversed:
      self.polarity = "inversed"
    self.tireradius = tireradius
    self.defaultSpeed = defaultSpeed
    self.stoptime = None
    self.stop_action = self.STOP_ACTION_BRAKE

  def tachosperinch(self):
    if self.tireradius:
      return self.count_per_rot/(2*math.pi*self.tireradius)
    else:
      print("Error: need tire radius")
      return

  def runMotorInchSecond(self, inches, seconds, wait = True):
    speed = self.tachosperinch() * inches / seconds
    if (speed > self.max_speed):
      print("Error: exceeds max speed")
      return
    else:
      self.runMotorSecondSpeed(speed = speed, seconds = seconds, wait = wait)

  def runMotorSpeedInch(self, inches, speed = None, wait = True):
    if not speed and not self.defaultSpeed:
      print("Error: no speed given")
      return
    elif not speed:
      speed = self.defaultSpeed
    seconds = abs(self.tachosperinch() * inches / speed)
    if speed*inches < 0:
      speed = -1 * abs(speed)
    else:
      speed = abs(speed)
    self.runMotorSecondSpeed(seconds = seconds, speed = speed, wait = wait)
    return seconds
  
  def runMotorSecondSpeed(self, seconds, speed = None, wait = True):
    if not speed and not self.defaultSpeed:
      print("Error: no speed given")
      return
    elif not speed:
      speed = self.defaultSpeed
    if wait:
      self.wait_until_not_moving()
    self.stoptime = datetime.datetime.now() + datetime.timedelta(seconds = seconds)
    self.run_timed(time_sp=seconds*1000, speed_sp=speed)



class TankCar():
  def __init__(self, left, right, axlelength = None):
    self.left = left
    self.right = right
    self.axlelength = axlelength
    self.stoptime = None
    
  def goStraight(self, speed = None, seconds = None, inches = None, wait = True):
    if speed and inches and seconds:
      print("Error: too many constraints")
      return
    elif speed and (speed > self.left.max_speed or speed > self.right.max_speed):
      print("Error: exceeds max speed")
      return    
    elif speed and seconds:
      self.left.runMotorSecondSpeed(seconds = seconds, speed = speed, wait = wait)
      self.right.runMotorSecondSpeed(seconds = seconds, speed = speed, wait = wait)
    elif inches and not (self.left.tireradius and self.right.tireradius):
      print("Error: set tire radius if using inches")
      return
    elif inches and seconds:
      self.left.runMotorInchSecond(seconds = seconds, inches = inches, wait = wait)
      self.right.runMotorInchSecond(seconds = seconds, inches = inches, wait = wait)
    elif inches and speed:
      self.left.runMotorSpeedInch(inches = inches, speed = speed, wait = wait)
      self.right.runMotorSpeedInch(inches = inches, speed = speed, wait = wait)
    elif inches:
      self.left.runMotorSpeedInch(inches = inches, wait = wait)
      self.right.runMotorSpeedInch(inches = inches, wait = wait)
    elif seconds:
      self.left.runMotorSecondSpeed(seconds = seconds, wait = wait)
      self.right.runMotorSecondSpeed(seconds = seconds, wait = wait)
    self.stoptime = self.left.stoptime
    return(self.stoptime)
  
  def TightTurn(self, direction, degrees = None, seconds = None, speed = None, wait = True):
    if direction.lower() not in ["left", "right"]:
      print("Error: directions must be 'left' or 'right'")
      return
    elif direction.lower() == "left":
      leftparity = -1
      rightparity = 1
    else:
      leftparity = 1
      rightparity = -1

    if degrees and not (self.left.tireradius and self.right.tireradius and self.axlelength):
      print("Error: must have tire radius and axle length set to calculate degrees")
      return
    else:
      inches = self.axlelength * math.pi * degrees/360

    if degrees and seconds and speed:
      print("Error: too many constraints")
    elif speed and (speed > self.left.max_speed) or (speed > self.right.max_speed):
      print("Error: exceeds max speed")
    elif speed and seconds:
      self.left.runMotorSecondSpeed(seconds = seconds, speed = leftparity * speed, wait = wait)
      self.right.runMotorSecondSpeed(seconds = seconds, speed = rightparity * speed, wait = wait)
    elif degrees and seconds:
      self.left.runMotorInchSecond(seconds = seconds, inches = inches, wait = wait)
      self.right.runMotorInchSecond(seconds = seconds, inches = inches, wait = wait)
    elif degrees and speed:
      self.left.runMotorSpeedInch(inches = inches, speed = leftparity * speed, wait = wait)
      self.right.runMotorSpeedInch(inches = inches, speed = rightparity * speed, wait = wait)
    elif degrees:
      self.left.runMotorSpeedInch(inches = leftparity * inches, wait = wait)
      self.right.runMotorSpeedInch(inches = rightparity * inches, wait = wait)
    elif seconds and (self.left.defaultSpeed and self.right.defaultSpeed):
      self.left.runMotorSecondSpeed(seconds = seconds, speed = leftparity * self.left.defaultSpeed, wait = wait)
      self.right.runMotorSecondSpeed(seconds = seconds, speed = rightparity * self.right.defaultSpeed, wait = wait)
    
    self.stoptime = self.left.stoptime
    return(self.stoptime)

  def Stop(self):
    self.left.stop()
    self.right.stop()
    self.stoptime = datetime.datetime.now()
    return(self.stoptime)
