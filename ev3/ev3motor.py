#!/usr/bin/env python3
from ev3dev.ev3 import *
import math


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

  def tachosperinch(self):
    if self.tireradius:
      return self.count_per_rot/(2*math.pi*self.tireradius)
    else:
      print("Error: need tire radius")
      return

  def runMotorInchSecond(self, inches, seconds):
    speed = self.tachosperinch() * inches / seconds
    if (speed > self.max_speed):
      print("Error: exceeds max speed")
      return
    else:
      self.runMotorSecondSpeed(speed = speed, seconds = seconds)

  def runMotorSpeedInch(self, inches, speed = None):
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
    self.runMotorSecondSpeed(seconds = seconds, speed = speed)
    return seconds
  
  def runMotorSecondSpeed(self, seconds, speed = None, wait=True):
    if not speed and not self.defaultSpeed:
      print("Error: no speed given")
      return
    elif not speed:
      speed = self.defaultSpeed
    if wait:
      self.wait_until_not_moving()
    self.run_timed(time_sp=seconds*1000, speed_sp=speed)



class TankCar():
  def __init__(self, left, right, axlelength = None):
    self.left = left
    self.right = right
    self.axlelength = axlelength
    
  def goStraight(self, speed = None, seconds = None, inches = None):
    if speed and inches and seconds:
      print("Error: too many constraints")
      return
    elif speed and (speed > self.left.max_speed or speed > self.right.max_speed):
      print("Error: exceeds max speed")
      return    
    elif speed and seconds:
      self.left.runMotorSecondSpeed(seconds = seconds, speed = speed)
      self.right.runMotorSecondSpeed(seconds = seconds, speed = speed)
    elif inches and not (self.left.tireradius and self.right.tireradius):
      print("Error: set tire radius if using inches")
      return
    elif inches and seconds:
      self.left.runMotorInchSecond(seconds = seconds, inches = inches)
      self.right.runMotorInchSecond(seconds = seconds, inches = inches)
    elif inches and speed:
      self.left.runMotorSpeedInch(inches = inches, speed = speed)
      self.right.runMotorSpeedInch(inches = inches, speed = speed)
    elif inches:
      self.left.runMotorSpeedInch(inches = inches)
      self.right.runMotorSpeedInch(inches = inches)
    elif seconds:
      self.left.runMotorSecondSpeed(seconds = seconds)
      self.right.runMotorSecondSpeed(seconds = seconds)
  
  def TightTurn(self, direction, degrees = None, seconds = None, speed = None):
    if direction.lower() not in ["left", "right"]:
      print("Error: directions must be 'left' or 'right'")
    elif degrees and seconds and speed:
      print("Error: too many constraints")
    elif speed and (speed > self.left.max_speed) or (speed > self.right.max_speed):
      print("Error: exceeds max speed")
      return    
