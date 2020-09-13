from datetime import date, datetime, timedelta
import RPi.GPIO as GPIO
import time

CLK = 17
data_in = 18
latch = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(latch, GPIO.OUT)  # latch
GPIO.setup(data_in, GPIO.OUT)  # data in
GPIO.setup(CLK, GPIO.OUT)  # clock
# setup IO
GPIO.output(latch, 0)
GPIO.output(CLK, 0)
GPIO.output(data_in, 0)


def pulseCLK():
    GPIO.output(CLK, 1)
    GPIO.output(CLK, 0)
    return


def putForward(m):
    GPIO.output(data_in, 1)
    serLatch()
    GPIO.output(data_in, 0)
    for m in range(0, m):
        serLatch()
    pulseCLK()
    return


def serLatch():
    GPIO.output(latch, 1)
    GPIO.output(latch, 0)
    return


def clearAll():
    for x in range(0, 32):
        GPIO.output(data_in, 0)
        serLatch()
    pulseCLK()
    return


def demo():
    for y in range(0, 32):
        clearAll()
        #  time.sleep(0.01)
        GPIO.output(data_in, 1)
        serLatch()
        for x in range(0, y):
            GPIO.output(data_in, 0)
            serLatch()
        pulseCLK()
        time.sleep(0.01)
    return


def display(h1, h2, m1, m2):
    bits = getBits(h1, h2, m1, m2)
    putForward(bits[0] - bits[1] - 1)
    putForward(bits[1] - bits[2] - 1)
    putForward(bits[2] - bits[3] - 1)
    putForward(bits[3])
    return


tube1 = {
    0: 19,
    1: 17,
    2: 18
}
tube2 = {
    0: 27,
    1: 20,
    2: 21,
    3: 22,
    4: 23,
    5: 16,
    6: 10,
    7: 30,
    8: 29,
    9: 28
}
tube3 = {
    0: 13,
    1: 12,
    2: 14,
    3: 15,
    4: 8,
    5: 26
}
tube4 = {
    0: 1,
    1: 9,
    2: 11,
    3: 0,
    4: 6,
    5: 7,
    6: 5,
    7: 4,
    8: 3,
    9: 2
}


def getBits(h1, h2, m1, m2):
    out = [tube1[h1], tube2[h2], tube3[m1], tube4[m2]]
    out.sort(reverse=True)
    return out


clearAll()

while 1:
    clearAll()
    now = datetime.now() + timedelta(hours=1)
    hours = str(now.strftime("%H"))
    minutes = str(now.strftime("%M"))
    display(int(hours[0]), int(hours[1]), int(minutes[0]), int(minutes[1]))
    time.sleep(1)
