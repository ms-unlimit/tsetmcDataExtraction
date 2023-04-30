import signal
import time

def signal_handler(signum, frame):
    raise Exception("Timed out!")
signal.signal(signal.SIGALRM, signal_handler)

time.sleep(1)
for i in range(0, 4):
    try:
        signal.alarm(2)
        time.sleep(i)
        print("done")
    except:
        print("Timed out!")
time.sleep(4)
print("end")
