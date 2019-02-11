#!/usr/bin/env python3
from ev3dev2.motor import *
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
  def __init__(self, port, reversed = 0, tireradius = None, defaultSpeed = 100):
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
    self.port = port.upper()
    if self.tireradius:
      self.setdegreesperinch()
      self.settachosperinch()

  def settachosperinch(self):
    if self.tireradius:
      self.tachosperinch = self.count_per_rot/(2 * math.pi * self.tireradius)
    else:
      print("Error: need tire radius")
      return

  def setdegreesperinch(self):
    if self.tireradius:
      self.degreesperinch = 360/(2*math.pi*self.tireradius)
    else:
      print("Error: need tire radius")
      return

  def speedgiveninchesseconds(self, inches, seconds):
    if self.tachosperinch:
      speed = self.tachosperinch * inches / seconds
      if speed > self.max_speed:
        print("Error: speed is greater than max_speed")
        return
      return speed
    else:
      print("Error: need tire radius")

  def runMotorInchSecond(self, inches, seconds, wait = True):
    speed = self.tachosperinch * inches / seconds
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
    seconds = abs(self.tachosperinch * inches / speed)
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

class TankCar(MoveTank):
  def __init__(self, left, right, axlelength = None, defaultspeed = 100):
    self.left = left
    self.right = right
    self.axlelength = axlelength
    self.stoptime = None
    self.defaultSpeed = defaultspeed
    MoveTank.__init__(self, left_motor_port = self.left.port, right_motor_port = self.right.port)
    
  def go(self, speed = None, seconds = None, inches = None, wait = True, leftparity = 1, rightparity = 1):
    
    if speed and inches and seconds:
      print("Error: too many constraints")
      return
    elif speed and (speed > self.left.max_speed or speed > self.right.max_speed):
      print("Error: exceeds max speed")
      return
    elif speed and seconds:
      self.on_for_seconds(left_speed = SpeedNativeUnits(leftparity * speed), right_speed = SpeedNativeUnits(rightparity * speed), seconds = seconds, brake=True, block=wait)
    elif inches and not (self.left.tireradius and self.right.tireradius):
      print("Error: set tire radius if using inches")
      return
    elif inches and seconds:
      self.on_for_degrees(left_speed = SpeedDPS(leftparity * inches * self.left.degreesperinch / seconds), right_speed = SpeedDPS(rightparity * inches * self.right.degreesperinch / seconds), degrees = inches*max(self.left.degreesperinch, self.right.degreesperinch), brake=True, block=True)
    elif inches and speed:
      self.on_for_degrees(left_speed = SpeedNativeUnits(leftparity * speed), right_speed = SpeedNativeUnits(rightparity * speed), degrees = inches*max(self.left.degreesperinch, self.right.degreesperinch), brake=True, block=True)
    elif inches:
      if self.defaultSpeed:
        self.on_for_degrees(left_speed = SpeedNativeUnits(leftparity * self.defaultSpeed), right_speed = SpeedNativeUnits(rightparity * self.defaultSpeed), degrees = inches*max(self.left.degressperinch, self.right.degreesperinch), brake=True, block=True)
      elif self.left.defaultSpeed and self.right.defaultSpeed:
        self.on_for_degrees(left_speed = SpeedNativeUnits(leftparity * self.left.defaultSpeed), right_speed = SpeedNativeUnits(rightparity * self.right.defaultSpeed), degrees = inches*max(self.left.degressperinch, self.right.degreesperinch), brake=True, block=True)
    elif seconds:
      self.left.runMotorSecondSpeed(seconds = seconds, wait = wait)
      self.right.runMotorSecondSpeed(seconds = seconds, wait = wait)
    
    if not seconds:
      seconds = inches/speed * self.left.tachosperinch
    self.stoptime = datetime.datetime.now() + datetime.timedelta(seconds = seconds)
    return(self.stoptime)
  
  def tightTurn(self, direction, degrees = None, seconds = None, speed = None, wait = True, gyro = None):
    if direction.lower() not in ["left", "right"]:
      print("Error: directions must be 'left' or 'right'")
      return
    elif direction.lower() == "left":
      leftparity = -1
      rightparity = 1
    else:
      leftparity = 1
      rightparity = -1
    
    gyro = None

    if not gyro:
      if degrees and not (self.left.tireradius and self.right.tireradius and self.axlelength):
        print("Error: must have tire radius and axle length set to calculate degrees")
        return
      else:
        inches = self.axlelength * math.pi * degrees/360
      self.go(speed = speed, seconds = seconds, inches = inches, wait = wait, leftparity = leftparity, rightparity = rightparity)
    
    return self.stoptime

  
  def Stop(self):
    self.left.stop()
    self.right.stop()
    self.stoptime = datetime.datetime.now()
    return(self.stoptime)

  