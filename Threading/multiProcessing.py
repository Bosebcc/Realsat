import multiprocessing
import time
state = 1
def sunTracking():
    global state
    for x in range(5):
        x = str(x)
        print("value" + x)
        time.sleep(0.5)
    state = 0
    return state
def barometer():
    print(state)
    '''
    while True:
        if state == True:
            print ("true")
            time.sleep(0.5)
        if state == False:
            print("break")
            break
    '''

if __name__ == '__main__':
    jobs = []
    sun = multiprocessing.Process(target=sunTracking)
    baro = multiprocessing.Process(target=barometer)
    jobs.append(sun)
    sun.start()
    sun.join()
    jobs.append(baro)
    baro.start()
    baro.join()
