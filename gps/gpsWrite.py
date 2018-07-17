import serial

gps = serial.Serial("/dev/ttyAMA0", baudrate = 9600)

while True:
    line = gps.readline()
    data = line.split(",")
    if data[0] == "$GPRMC":
        if data[2] == "A":
            with open("position.txt", "w") as pos:
                pos.write("%s,%s\n" % ( data[3], data[5]))
