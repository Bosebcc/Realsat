import serial

gps = serial.Serial("/dev/ttyAMA0", baudrate = 9600)

while True:
    line = gps.read()
    data = line.split(",")
    if data[0] == "$GPRMC":
        if data[2] == "A":
            print "Latitude: %s" %( data[3] )
            print "Longtitude: %s" %( data[5] )
