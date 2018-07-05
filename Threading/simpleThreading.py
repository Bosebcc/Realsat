import threading
import time

class sunTracking(threading.Thread):
    print ("Starting sunTracking")

thread1 = sunTracking(1, "Thread-1", 1)

thread1.start()

print ("Exiting Main Thread")
