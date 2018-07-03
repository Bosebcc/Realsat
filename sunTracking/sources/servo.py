import pigpio
pi = pigpio.pi()
import RPi.GPIO as GPIO
gpioServo = 4

pi.set_servo_pulsewidth(gpioServo, 500)

'''
for x in range(21):
    pulse = (x * 100)+500
    time.sleep(0.5)'''
