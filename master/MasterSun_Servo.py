#Barometer
import math

#Multithreading
import thread
import threading
from threading import *

#Multiproccesing
import multiprocessing

# Variables
getAltitude = None
sea_press = 1013.25

# Interface

I2C=0
SPI=1

AUX_SPI=256

# Barometer Sampling

OVER_SAMPLE_1 = 1
OVER_SAMPLE_2 = 2
OVER_SAMPLE_4 = 3
OVER_SAMPLE_8 = 4
OVER_SAMPLE_16 = 5
stateSun = True


#StepperMotor
import pigpio

#servo
pulse = None
gpioServo = 4
servoPos = None

#Grove Sunlight Sensor
import sys
import os
pulse = None
gpioServo = 4
servoPos = None
highVisible = 0
uvIrradiance = None
stepPos = None

sys.path.append('./SDL_Pi_SI1145');
import time
from time import sleep

#servo
pi = pigpio.pi()
import RPi.GPIO as GPIO

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

LED = 4

GPIO.setup(LED, GPIO.OUT, initial=0)

from datetime import datetime

class sensor:
   """
   A class to read the BME280 pressure, humidity, and temperature sensor._
   """

   # BME280 Registers

   _calib00    = 0x88

   _T1         = 0x88 - _calib00
   _T2         = 0x8A - _calib00
   _T3         = 0x8C - _calib00

   _P1         = 0x8E - _calib00
   _P2         = 0x90 - _calib00
   _P3         = 0x92 - _calib00
   _P4         = 0x94 - _calib00
   _P5         = 0x96 - _calib00
   _P6         = 0x98 - _calib00
   _P7         = 0x9A - _calib00
   _P8         = 0x9C - _calib00
   _P9         = 0x9E - _calib00

   _H1         = 0xA1 - _calib00

   _chip_id    = 0xD0
   _reset      = 0xE0

   _calib26    = 0xE1

   _H2         = 0xE1 - _calib26
   _H3         = 0xE3 - _calib26
   _xE4        = 0xE4 - _calib26
   _xE5        = 0xE5 - _calib26
   _xE6        = 0xE6 - _calib26
   _H6         = 0xE7 - _calib26

   _ctrl_hum   = 0xF2
   _status     = 0xF3
   _ctrl_meas  = 0xF4
   _config     = 0xF5

   _rawdata    = 0xF7

   _p_msb      = 0xF7 - _rawdata
   _p_lsb      = 0xF8 - _rawdata
   _p_xlsb     = 0xF9 - _rawdata
   _t_msb      = 0xFA - _rawdata
   _t_lsb      = 0xFB - _rawdata
   _t_xlsb     = 0xFC - _rawdata
   _h_msb      = 0xFD - _rawdata
   _h_lsb      = 0xFE - _rawdata

   _os_ms = [0, 1, 2, 4, 8, 16]

   def __init__(self, pi, sampling=OVER_SAMPLE_1, interface=I2C,
                   bus=1, address=0x76,
                   channel=0, baud=10000000, flags=0):

      self.pi = pi

      if interface == I2C:
         self.I2C = True
      else:
         self.I2C = False

      self.sampling = sampling

      if self.I2C:
         self.h = pi.i2c_open(bus, address)
      else:
         self.h = pi.spi_open(channel, baud, flags)

      self._load_calibration()

      self.measure_delay = self._measurement_time(sampling, sampling, sampling)

      self.t_fine = 0.0

   def _measurement_time(self, os_temp, os_press, os_hum):
      ms = ( (1.25  + 2.3 * sensor._os_ms[os_temp]) +
             (0.575 + 2.3 * sensor._os_ms[os_press]) +
             (0.575 + 2.3 * sensor._os_ms[os_hum]) )
      return (ms/1000.0)

   def _u16(self, _calib, off):
      return (_calib[off] | (_calib[off+1]<<8))

   def _s16(self, _calib, off):
      v = self._u16(_calib, off)
      if v > 32767:
         v -= 65536
      return v

   def _u8(self, _calib, off):
      return _calib[off]

   def _s8(self, _calib, off):
      v = self._u8(_calib,off)
      if v > 127:
         v -= 256
      return v

   def _write_registers(self, data):
      if self.I2C:
         self.pi.i2c_write_device(self.h, data)
      else:
         for i in range(0, len(data), 2):
            data[i] &= 0x7F
         self.pi.spi_xfer(self.h, data)

   def _read_registers(self, reg, count):
      if self.I2C:
         return self.pi.i2c_read_i2c_block_data(self.h, reg, count)
      else:
         c, d = self.pi.spi_xfer(self.h, [reg|0x80] + [0]*count)
         if c > 0:
            return c-1, d[1:]
         else:
            return c, d

   def _load_calibration(self):

      c, d1 = self._read_registers(sensor._calib00, 26)

      self.T1 = self._u16(d1, sensor._T1)
      self.T2 = self._s16(d1, sensor._T2)
      self.T3 = self._s16(d1, sensor._T3)

      self.P1 = self._u16(d1, sensor._P1)
      self.P2 = self._s16(d1, sensor._P2)
      self.P3 = self._s16(d1, sensor._P3)
      self.P4 = self._s16(d1, sensor._P4)
      self.P5 = self._s16(d1, sensor._P5)
      self.P6 = self._s16(d1, sensor._P6)
      self.P7 = self._s16(d1, sensor._P7)
      self.P8 = self._s16(d1, sensor._P8)
      self.P9 = self._s16(d1, sensor._P9)

      self.H1 = self._u8(d1, sensor._H1)

      c, d2 = self._read_registers(sensor._calib26, 7)

      self.H2 = self._s16(d2, sensor._H2)

      self.H3 = self._u8(d2, sensor._H3)

      t = self._u8(d2, sensor._xE5)

      t_l = t & 15
      t_h = (t >> 4) & 15

      self.H4 = (self._u8(d2, sensor._xE4) << 4) | t_l

      if self.H4 > 2047:
         self.H4 -= 4096

      self.H5 = (self._u8(d2, sensor._xE6) << 4) | t_h

      if self.H5 > 2047:
         self.H5 -= 4096

      self.H6 = self._s8(d2, sensor._H6)

   def _read_raw_data(self):

      # Set oversampling rate and force reading.

      self._write_registers(
         [sensor._ctrl_hum, self.sampling,
          sensor._ctrl_meas, self.sampling << 5 | self.sampling << 2 | 1])

      # Measurement delay.

      time.sleep(self.measure_delay)

      # Grab reading.

      c, d = self._read_registers(sensor._rawdata, 8)

      msb = self._u8(d, sensor._t_msb)
      lsb = self._u8(d, sensor._t_lsb)
      xlsb = self._u8(d, sensor._t_xlsb)
      raw_t = ((msb << 16) | (lsb << 8) | xlsb) >> 4

      msb = self._u8(d, sensor._p_msb)
      lsb = self._u8(d, sensor._p_lsb)
      xlsb = self._u8(d, sensor._p_xlsb)
      raw_p = ((msb << 16) | (lsb << 8) | xlsb) >> 4

      msb = self._u8(d, sensor._h_msb)
      lsb = self._u8(d, sensor._h_lsb)
      raw_h = (msb << 8) | lsb

      return raw_t, raw_p, raw_h

   def read_data(self):
      """
      Returns the temperature, pressure, and humidity as a tuple.

      Each value is a float.

      The temperature is returned in degrees centigrade.  The
      pressure is returned in Pascals.  The humidity is returned
      as the relative humidity between 0 and 100%.
      """

      raw_t, raw_p, raw_h = self._read_raw_data()

      var1 = (raw_t/16384.0 - (self.T1)/1024.0) * float(self.T2)
      var2 = (((raw_t)/131072.0 - (self.T1)/8192.0) *
              ((raw_t)/131072.0 - (self.T1)/8192.0)) * (self.T3)

      self.t_fine = var1 + var2

      t = (var1 + var2) / 5120.0

      var1 = (self.t_fine/2.0) - 64000.0
      var2 = var1 * var1 * self.P6 / 32768.0
      var2 = var2 + (var1 * self.P5 * 2.0)
      var2 = (var2/4.0)+(self.P4 * 65536.0)
      var1 = ((self.P3 * var1 * var1 / 524288.0) + (self.P2 * var1)) / 524288.0
      var1 = (1.0 + var1 / 32768.0)*self.P1
      if var1 != 0.0:
         p = 1048576.0 - raw_p
         p = (p - (var2 / 4096.0)) * 6250.0 / var1
         var1 = self.P9 * p * p / 2147483648.0
         var2 = p * self.P8 / 32768.0
         p = p + (var1 + var2 + self.P7) / 16.0
      else:
         p = 0

      h = self.t_fine - 76800.0

      h = ( (raw_h - ((self.H4) * 64.0 + (self.H5) / 16384.0 * h)) *
            ((self.H2) / 65536.0 * (1.0 + (self.H6) / 67108864.0 * h *
            (1.0 + (self.H3) / 67108864.0 * h))))

      h = h * (1.0 - self.H1 * h / 524288.0)

      if h > 100.0:
         h = 100.0
      elif h < 0.0:
         h = 0.0

      return t, p, h

   def cancel(self):
      """
      Cancels the sensor and releases resources.
      """
      if self.h is not None:

         if self.I2C:
            self.pi.i2c_close(self.h)
         else:
            self.pi.spi_close(self.h)

         self.h = None

def barometer():
   import time
   import BME280
   import pigpio
   global stateSun

   pi = pigpio.pi()

   if not pi.connected:
      exit(0)

   s = BME280.sensor(pi)

   stop = time.time() + 60
   if stateSun == True:
    while stop > time.time():
       t, p, h = s.read_data()
       getAltitude = ((math.pow((sea_press / (p/100.0)), 1/5.257) - 1.0) * (t + 273.15)) / 0.0065; #Pressure to Altitude Equation
       print("h={:.2f} p={:.2f} t={:.2f} Alt={:.1f}".format(h, p/100.0, t, getAltitude)) #:.2f set decimal to 2 places
       time.sleep(0.9)
   else:
    s.cancel()
    return

class Motor(object):
    def __init__(self, pins, mode=3):
        """Initialise the motor object.

        pins -- a list of 4 integers referring to the GPIO pins that the IN1, IN2
                IN3 and IN4 pins of the ULN2003 board are wired to
        mode -- the stepping mode to use:
                1: wave drive (not yet implemented)
                2: full step drive
                3: half step drive (default)

        """
        self.P1 = pins[0]
        self.P2 = pins[1]
        self.P3 = pins[2]
        self.P4 = pins[3]
        self.mode = mode
        self.deg_per_step = 5.625 / 64  # for half-step drive (mode 3)
        self.steps_per_rev = int(360 / self.deg_per_step)  # 4096
        self.step_angle = 0  # Assume the way it is pointing is zero degrees
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

    def _set_rpm(self, rpm):
        """Set the turn speed in RPM."""
        self._rpm = rpm
        # T is the amount of time to stop between signals
        self._T = (60.0 / rpm) / self.steps_per_rev

    # This means you can set "rpm" as if it is an attribute and
    # behind the scenes it sets the _T attribute
    rpm = property(lambda self: self._rpm, _set_rpm)

    def move_to(self, angle):
        """Take the shortest route to a particular angle (degrees)."""
        # Make sure there is a 1:1 mapping between angle and stepper angle
        target_step_angle = 8 * (int(angle / self.deg_per_step) / 8)
        steps = target_step_angle - self.step_angle
        steps = (steps % self.steps_per_rev)
        if steps > self.steps_per_rev / 2:
            steps -= self.steps_per_rev
            print "moving " + `steps` + " steps"
            if self.mode == 2:
                self._move_acw_2(-steps / 8)
            else:
                self._move_acw_3(-steps / 8)
        else:
            print "moving " + `steps` + " steps"
            if self.mode == 2:
                self._move_cw_2(steps / 8)
            else:
                self._move_cw_3(steps / 8)
        self.step_angle = target_step_angle

    def __clear(self):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

    def _move_acw_2(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P3, 0)
            GPIO.output(self.P1, 1)
            sleep(self._T * 2)
            GPIO.output(self.P2, 0)
            GPIO.output(self.P4, 1)
            sleep(self._T * 2)
            GPIO.output(self.P1, 0)
            GPIO.output(self.P3, 1)
            sleep(self._T * 2)
            GPIO.output(self.P4, 0)
            GPIO.output(self.P2, 1)
            sleep(self._T * 2)

    def _move_cw_2(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P4, 0)
            GPIO.output(self.P2, 1)
            sleep(self._T * 2)
            GPIO.output(self.P1, 0)
            GPIO.output(self.P3, 1)
            sleep(self._T * 2)
            GPIO.output(self.P2, 0)
            GPIO.output(self.P4, 1)
            sleep(self._T * 2)
            GPIO.output(self.P3, 0)
            GPIO.output(self.P1, 1)
            sleep(self._T * 2)

    def _move_acw_3(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)

    def _move_cw_3(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)

#SunLight
import SDL_Pi_SI1145
sensor = SDL_Pi_SI1145.SDL_Pi_SI1145()

def readSunLight():

        vis = sensor.readVisible()
        IR = sensor.readIR()
        UV = sensor.readUV()
        uvIndex = UV / 100.0
        print('SunLight Sensor read at time: %s' % datetime.now())
        print '		Vis:             ' + str(vis)
        print '		IR:              ' + str(IR)
        print '		UV Index:        ' + str(uvIndex)

        #Warning
        if uvIndex <= 3 :
            print "Warning:" + "Wear Sun Glass; Low UV"
        elif uvIndex > 3 and uvIndex <= 6 :
            print "Warning:" + "Take cover when avalible; Moderate UV"
        elif uvIndex > 6 and uvIndex >= 8 :
            print "Warning:" + "Apply SPF 30+ sunscreen, don't stay out more than 3 hours; High UV"
        elif uvIndex > 8 and uvIndex >= 11 :
            print "Warning:" + "Do not stay in the sun for too long; Very High UV"
        else :
            print "Warning:" + "Take all Percautions; Extreme UV"

        #uvIrradiance
        #uvIrradiance = uvIndex * 0.025
        #print "Uv Irradiance: " + uvIrradiance

	returnValue = []
	returnValue.append(vis)
	returnValue.append(IR)
	returnValue.append(uvIndex)
	return returnValue

def sunTracking():
    global highVisible, stepPos, servoPos, uvIndex, vis, IR, UV, pulse, stateSun
    GPIO.setmode(GPIO.BCM)
    m = Motor([6,13,19,26])
    m.rpm = 10
    print "Pause in seconds: " + `m._T`
    #stepper
    for numOfTurn in range(24):
        degreeOfTurn = numOfTurn*15
        m.move_to(degreeOfTurn)
        for x in range(21):
            if x <= 1:
                pulse = (x * 100)+500
                pi.set_servo_pulsewidth(gpioServo, pulse)
                time.sleep(0.3)
                vis = sensor.readVisible()
                IR = sensor.readIR()
                UV = sensor.readUV()
                uvIndex = UV / 100.0
                if highVisible < uvIndex:
                    servoPos = x
                    stepPos = degreeOfTurn
                    highVisible = uvIndex
                    pass
                #print('SunLight Sensor read at time: %s' % datetime.now())
                #print '		Vis:             ' + str(vis)
                #print '		IR:              ' + str(IR)
                #print '		UV Index:        ' + str(uvIndex)
            else:
                pulse = (x * 100)+500   #turn  servo 100 pulse from 500-2500
                pi.set_servo_pulsewidth(gpioServo, pulse)
                time.sleep(0.015)
                vis = sensor.readVisible()
                IR = sensor.readIR()
                UV = sensor.readUV()
                uvIndex = UV / 100.0
                if highVisible < uvIndex:
                    servoPos = x
                    stepPos = degreeOfTurn
                    highVisible = uvIndex
                    pass
                #print('SunLight Sensor read at time: %s' % datetime.now())
                #print '		Vis:             ' + str(vis)
                #print '		IR:              ' + str(IR)
                #print '		UV Index:        ' + str(uvIndex)
    servoPos = (servoPos * 100)+500
    pi.set_servo_pulsewidth(gpioServo, servoPos)
    print(servoPos)
    m.move_to(stepPos)
    time.sleep(1)
    pi.set_servo_pulsewidth(gpioServo, 0)
    #calculating effect on human
    uvIrradiance = highVisible * 0.025 * 60 * 10
    print "Uv Irradiance: " + str(uvIrradiance)
    if uvIrradiance > 2.67 :
        print "Your skin will start to burn and tanning under 15 minutes, please find a place to hide from uv now"
    elif uvIrradiance <= 2.67 and uvIrradiance > 1.33 :
        print "Your skin will start to burn and tanning within 15 minutes"
    elif uvIrradiance <= 1.33 and uvIrradiance > 0.89 :
        print "Your skin will start to burn and tanning within half an hour"
    elif uvIrradiance <= 0.89 and uvIrradiance > 0.67 :
        print "Your skin will start to burn and tanning within 45 minutes"
    else :
        print "Your skin will start to burn and tanning within an hour"
    #print("Ps. This case is for Mediterranean, Asian and Latino people only")
    stateSun = False
    return stateSun

if __name__ == '__main__':
    jobs = []
    sun = multiprocessing.Process(target=sunTracking)
    baro = multiprocessing.Process(target=barometer)
    jobs.append(sun)
    jobs.append(baro)
    sun.start()
    baro.start()
    sun.join()
    baro.join()

    #data management
    ctime = str(time.ctime(time.time()))
    uv = str(highVisible)
    file = open("sunlightdata.txt")
    file.write("Highest UV")
    file.write(ctime + "/n")
    file.write(highVisible)

    file.close()

    pi.stop()
    GPIO.cleanup()
