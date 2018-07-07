import pigpio
pi = pigpio.pi()
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

if __name__ == '__main__':
    pi.stop()
    GPIO.cleanup()
