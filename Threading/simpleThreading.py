import threading
import time

x = 0

class sunTracking(threading.Thread):
    print ("Starting sunTracking")

def repeat():
    while(True):
        print ("Repeat")
        time.sleep(1)

thread1 = sunTracking()
thread2 = threading.Timer(1, repeat)
thread1.start()
thread2.start()

print ("Exiting Main Thread")
