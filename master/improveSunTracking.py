for numOfTurn in range(19):
    degreeOfTurn = numOfTurn*20
    m.move_to(degreeOfTurn)
    if servoTurnDirection == clockwise:
        for x in range(21):
            pulse = (x * 100)+500
            pi.set_servo_pulsewidth(gpioServo, pulse)
            time.sleep(servoDelay)
            vis = sensor.readVisible()
            IR = sensor.readIR()
            UV = sensor.readUV()

            uvIndex = UV / 100.0

            #Log " Time  , Alt  ,  UV  , Steppper , Servo , Temp , Pressure , Humidity "
            ctime = str(time.ctime(time.time()))
            uvLog = str(uvIndex)
            altitudeLog = str(getAltitude)
            pulseLog = str(pulse)
            stepperPosCurrent = 0
            stepperPosCurrent += degreeOfTurn
            stepperLog = str(stepperPosCurrent)

            if highVisible < uvIndex:
                servoPos = x
                stepPos = degreeOfTurn
                highVisible = uvIndex
                pass
            #print('SunLight Sensor read at time: %s' % datetime.now())
            #print '		Vis:             ' + str(vis)
            #print '		IR:              ' + str(IR)
            #print '		UV Index:        ' + str(uvIndex)
        servoPos = (servoPos * 100)+500
        pi.set_servo_pulsewidth(gpioServo, servoPos)
        print(servoPos)
        m.move_to(stepPos)
        time.sleep(1)
        pi.set_servo_pulsewidth(gpioServo, 0)
        #calculating effect on human
        uvIrradiance = highVisible * 0.025 * 60 / 10
        print "Uv Irradiance: " + str(uvIrradiance)
        if uvIrradiance > 2.67 :
            print "Your skin will start to burn and tanning under 15 minutes, please find a place to hide from uv now"
        elif uvIrradiance <= 2.67 and uvIrradiance > 1.33 :
            print "Your skin will start to burn and tanning within 15 minutes"
        elif uvIrradiance <= 1.33 and uvIrradiance > 0.89 :
            print "Your skin will start to burn and tanning within half an hour"
        elif uvIrradiance <= 0.89 and uvIrradiance > 0.67 :
            print "Your skin will start to burn and tanning within an hour"
        else :
            print "Your skin will start to burn and tanning more than an hour"
        #print("Ps. This case is for Mediterranean, Asian and Latino people only")

    if servoTurnDirection == counterClockwise:
        for x in range(21):
            pulse = 2500-(x * 100)
            pi.set_servo_pulsewidth(gpioServo, pulse)
            time.sleep(servoDelay)
            vis = sensor.readVisible()
            IR = sensor.readIR()
            UV = sensor.readUV()

            uvIndex = UV / 100.0

            #Log " Time  , Alt  ,  UV  , Steppper , Servo , Temp , Pressure , Humidity "
            ctime = str(time.ctime(time.time()))
            uvLog = str(uvIndex)
            altitudeLog = str(getAltitude)
            pulseLog = str(pulse)
            stepperPosCurrent = 0
            stepperPosCurrent += degreeOfTurn
            stepperLog = str(stepperPosCurrent)

            if highVisible < uvIndex:
                servoPos = x
                stepPos = degreeOfTurn
                highVisible = uvIndex
                pass
            #print('SunLight Sensor read at time: %s' % datetime.now())
            #print '		Vis:             ' + str(vis)
            #print '		IR:              ' + str(IR)
            #print '		UV Index:        ' + str(uvIndex)
        servoPos = (servoPos * 100)+500
        pi.set_servo_pulsewidth(gpioServo, servoPos)
        print(servoPos)
        m.move_to(stepPos)
        time.sleep(1)
        pi.set_servo_pulsewidth(gpioServo, 0)
        #calculating effect on human
        uvIrradiance = highVisible * 0.025 * 60 / 10
        print "Uv Irradiance: " + str(uvIrradiance)
        if uvIrradiance > 2.67 :
            print "Your skin will start to burn and tanning under 15 minutes, please find a place to hide from uv now"
        elif uvIrradiance <= 2.67 and uvIrradiance > 1.33 :
            print "Your skin will start to burn and tanning within 15 minutes"
        elif uvIrradiance <= 1.33 and uvIrradiance > 0.89 :
            print "Your skin will start to burn and tanning within half an hour"
        elif uvIrradiance <= 0.89 and uvIrradiance > 0.67 :
            print "Your skin will start to burn and tanning within an hour"
        else :
            print "Your skin will start to burn and tanning more than an hour"
        #print("Ps. This case is for Mediterranean, Asian and Latino people only")
    stateSun = False
