import pigpio
from PigpioStepperMotor import StepperMotor, fullStepSequence

pi = pigpio.pi()
motor = StepperMotor(pi, 6, 13, 19, 26, sequence = fullStepSequence)
for i in range(1024):
  motor.doCounterclockwiseStepClockwiseStep()
