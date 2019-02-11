import ev3.ev3motor as ev3
from ev3dev2.sensor.lego import *
from ev3dev2.sound import *

# A library for interacting with the EV3 Education Sensor Car.  

class SensorCar(ev3.TankCar):
  def __init__(self, tireradius = .73, axlelength = 3.9, leftmotorport = "B", rightmotorport = "C"):
    if leftmotorport.upper() not in ["A", "B", "C", "D"]:
      print("Error: Port must be A, B, C, or D")
      return
    if rightmotorport.upper() not in ["A", "B", "C", "D"]:
      print("Error: Port must be A, B, C, or D")
      return
    left = ev3.MyMotor(port = leftmotorport.upper(), tireradius = tireradius)
    right = ev3.MyMotor(port = rightmotorport.upper(), tireradius = tireradius)

    self.getSensors()
    self.sound = Sound()

    ev3.TankCar.__init__(self, left, right, axlelength = axlelength)
  
  def getSensors(self):
    try:
      self.touch = TouchSensor()
    except:
      self.touch = None
    try:
      self.color = ColorSensor()
    except:
      self.color = None
    try:
      self.gyro = GyroSensor()
    except:
      self.gyro = None
    try:
      self.sonic = UltrasonicSensor()
    except:
      self.sonic = None
    try:
      self.ir = InfraredSensor()
    except:
      self.ir = None

