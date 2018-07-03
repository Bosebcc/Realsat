import pigpio
from PigpioStepperMotor import StepperMotor, fullStepSequence
import time

#Variables
previousTime = 0
interval = 0.5
delaystate = False
currentTime = time.time()
pi = pigpio.pi()
motor = StepperMotor(pi, 6, 13, 19, 26, sequence = fullStepSequence, delayAfterStep = 0)
for i in range(256):
    if currentTime - previousTime > interval :
        # save the last time the servo turn
        previousTime = currentTime
        if delaystate == False :
            delayState = True
            motor.doCounterclockwiseStep()
            motor.doCounterclockwiseStep()
            motor.doCounterclockwiseStep()
            motor.doCounterclockwiseStep()
        else :
            delayState = False
