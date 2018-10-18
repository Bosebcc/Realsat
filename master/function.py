class barometer:
    def barometer(self):
	import sys
	sys.path.insert(0,'lib/')
	import time
        import BME280
	import pigpio
 	import math

	getAltitude = None
	sea_press = 1013.25

	pi = pigpio.pi()

	if not pi.connected:
	   exit(0)

        s = BME280.sensor(pi)

        stop = time.time() + 60

        while stop > time.time():
           t, p, h = s.read_data()
           getAltitude = ((math.pow((sea_press / (p/100.0)), 1/5.257) - 1.0) * (t + 273.15)) / 0.0065; #Pressure to Altitude Equation
           print("h={:.2f} p={:.2f} t={:.2f} Alt={:.1f}".format(h, p/100.0, t, getAltitude)) #:.2f set decimal to 2 places
           time.sleep(0.9)

        s.cancel()
