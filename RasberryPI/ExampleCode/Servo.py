import time

import pigpio

pi = pigpio.pi() # Connect to local Pi.

for x in range(2,6):
    print(x+1)
    pass

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

'''
pi.set_servo_pulsewidth(4, 1000)
time.sleep(2)
pi.set_servo_pulsewidth(4, 1500)
time.sleep(2)
pi.set_servo_pulsewidth(4, 2000)
time.sleep(2)
pi.set_servo_pulsewidth(4, 1500)
time.sleep(2)

# switch servo off
pi.set_servo_pulsewidth(4, 0);
'''

pi.stop()
