import ev3.ev3motor as ev3

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

    self.touch = ev3.TouchSensor()
    self.color = ev3.ColorSensor()
    self.gyro = ev3.GyroSensor()
    self.sonic = ev3.UltrasonicSensor()
    self.ir = ev3.InfraredSensor()
    
    self.sound = ev3.Sound()

    ev3.TankCar.__init__(self, left, right, axlelength = axlelength)
