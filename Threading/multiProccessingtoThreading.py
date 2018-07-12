from threading import Thread
import time
state = 1

def sunTracking():
    global state
    for x in range(5):
        x = str(x)
        print("value" + x)
        time.sleep(0.5)
    state = 0
def barometer():
    print(state)
    while True:
        if state == True:
            print ("true")
            time.sleep(0.5)
        if state == False:
            print("break")
            break


if __name__ == '__main__':
    jobs = []
    sun = Thread(target=sunTracking)
    baro = Thread(target=barometer)
    jobs.append(sun)
    jobs.append(baro)
    baro.start()
    sun.start()
    sun.join()
    baro.join()
