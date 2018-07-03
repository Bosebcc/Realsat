import time
import sys
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
y = 1

def number():
    y+=1
    print(y)

def timeRightnow():
    print (time.time())

def killLogger():
    scheduler.shutdown()
    print "Scheduler Shutdown...."
    exit()

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(number, 'interval', seconds=3)
    scheduler.add_job(timeRightnow, 'interval', seconds=2)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
