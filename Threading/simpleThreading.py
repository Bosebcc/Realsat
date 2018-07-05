import threading
import time

class sunTracking(threading.Thread):
    print ("Starting sunTracking")

thread1 = sunTracking()

thread1.start()

print ("Exiting Main Thread")
