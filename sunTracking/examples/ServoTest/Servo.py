import time
import SDL_Pi_SI1145
import pigpio

sensor = SDL_Pi_SI1145.SDL_Pi_SI1145()
from datetime import datetime

pi = pigpio.pi() # Connect to local Pi.

pulse = None
gpioServo = 4
servoPos = None
highVisible = 0

for x in range(21):
    pulse = (x * 100)+500   #turn  servo 100 pulse from 500-2500
    pi.set_servo_pulsewidth(gpioServo, pulse)
    print(servoPos)
    time.sleep(0.4)
    vis = sensor.readVisible()
    IR = sensor.readIR()
    UV = sensor.readUV()
    uvIndex = UV / 100.0
    if highVisible < uvIndex:
        servoPos = x
        highVisible = uvIndex
        pass
    print('SunLight Sensor read at time: %s' % datetime.now())
    print '		Vis:             ' + str(vis)
    print '		IR:              ' + str(IR)
    print '		UV Index:        ' + str(uvIndex)

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
    pass

if __name__ == '__main__':
    servoPos = (servoPos * 100)+500
    pi.set_servo_pulsewidth(gpioServo, servoPos)
    print(servoPos)
    time.sleep(1)
    pi.set_servo_pulsewidth(gpioServo, 0)
    pi.stop()

'''
for x in range(21):
    if x == 21:
        break
    else :
        pulse = (x * 100)+500   #turn  servo 100 pulse from 500-2500
        servoPos = x*9
        pi.set_servo_pulsewidth(gpioServo, pulse)
        print(servoPos)
        time.sleep(0.4)
        pass
'''

'''
pi.set_servo_pulsewidth(gpioServo, 1000)
time.sleep(2)
pi.set_servo_pulsewidth(gpioServo, 1500)
time.sleep(2)
pi.set_servo_pulsewidth(gpioServo, 2000)
time.sleep(2)
pi.set_servo_pulsewidth(gpioServo, 1500)
time.sleep(2)

# switch servo off
pi.set_servo_pulsewidth(4, 0);
'''
