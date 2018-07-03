pi = pigpio.pi()
import RPi.GPIO as GPIO

pi.set_servo_pulsewidth(gpioServo, 500)

'''
for x in range(21):
    pulse = (x * 100)+500
    time.sleep(0.5)'''
