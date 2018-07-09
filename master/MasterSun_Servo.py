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


import SDL_Pi_SI1145

sensor = SDL_Pi_SI1145.SDL_Pi_SI1145()

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
            movingsteps = "moving " + `steps` + " steps"
            print movingsteps
            if self.mode == 2:
                self._move_acw_2(-steps / 8)
            else:
                self._move_acw_3(-steps / 8)
        else:
            movingsteps2 = "moving " + `steps` + " steps"
            print movingsteps2
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

def readSunLight():

        vis = sensor.readVisible()
        IR = sensor.readIR()
        UV = sensor.readUV()
        uvIndex = UV / 100.0
        sunsensor = ('SunLight Sensor read at time: %s' % datetime.now())
        Visual =    "		Vis:             " + str(vis)
        IR =        "		IR:              " + str(IR)
        uvindex1 =  "		UV Index:        " + str(uvIndex)
        print sunsensor
        print Visual
        print IR
        print uvindex1

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

if __name__ == "__main__":
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
                sunsensor = ('SunLight Sensor read at time: %s' % datetime.now())
                Visual =    "		Vis:             " + str(vis)
                IR =        "		IR:              " + str(IR)
                uvindex1 =  "		UV Index:        " + str(uvIndex)
                print sunsensor
                print sunsensor
                print Visual
                print IR
                print uvindex1
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
                sunsensor = ('SunLight Sensor read at time: %s' % datetime.now())
                Visual =    "		Vis:             " + str(vis)
                IR =        "		IR:              " + str(IR)
                uvindex1 =  "		UV Index:        " + str(uvIndex)
                print sunsensor
                print sunsensor
                print Visual
                print IR
                print uvindex1
    servoPos = (servoPos * 100)+500
    pi.set_servo_pulsewidth(gpioServo, servoPos)
    print(servoPos)
    m.move_to(stepPos)
    time.sleep(1)
    pi.set_servo_pulsewidth(gpioServo, 0)
    pi.stop()
    GPIO.cleanup()

# Storing Data Section
f = open()



###  Check if it correct
#        uvIrradiance
#        #(dont use this line)uvIrradiance = uvIndex * 0.025 * 60(seconds) * 10 (J/m^2 to mJ/cm^2)
#            uvIrradiance = uvIndex * 0.025 * 60 * 10
#            print "Uv Irradiance: " + uvIrradiance
#         #so we will get UV Dose per minute by multiplying 60 seconds
#
#            if uvIrradiance > 2.67 :
#                print "Human skin will start to burn and tanning under 15 minutes."
#            elif uvIrradiance <= 2.67 > 1.33 :
#                print "Human skin will start to burn and tanning within 15 minutes."
#            elif uvIrradiance <= 1.33 > 0.89 :
#                print "Human skin will start to burn and tanning within half an hour."
#            elif uvIrradiance <= 0.89 > 0.67 :
#                print "Human skin will start to burn and tanning within 45 minutes."
#            else uvIrradiance <= 0.67 :
#                print "Human skin will start to burn and tanning within an hour."
#
#
#       print("Ps. This case is for Mediterranean, Asian and Latino people only")
###
