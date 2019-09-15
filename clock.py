# This file is based on pybike project
# https://www.hackster.io/user83346052/pybike-2fa1dd

class RotationCounter:
   def __init__(self, pin, debounce_ms):
       self._pin = Pin(pin, mode=Pin.IN, pull=Pin.PULL_DOWN)
       self._debounce_ms = debounce_ms
       self._last_count_ms = None
       self._pin.callback(Pin.IRQ_RISING, self._handler)
       self.counter = 0

   def _handler(self, pin):
       time_ms = time.ticks_ms()
       if ((self._last_count_ms is not None) and
               (time_ms - self._last_count_ms > self._debounce_ms)):
           self.counter += 1
           self._last_count_ms = None
       else:
           self._last_count_ms = time_ms

class Clock:
    def __init__(self, counter_pin):
        self.rt = RotationCounter(counter_pin, 30)
        self.currentDist = 0
        self.finish = False
        self.prevDist = 0
        self.distTravelled = 0
        self.notify = True
        self.speed = 0
        self.seconds = 0

    def _seconds_handler(self, alarm):
        self.currentDist = (self.rt.counter * 2.07)
        # Calculate the remaining distance
        self.seconds += 1

        if (self.seconds % 5 == 0):
            self.distTravelled = self.currentDist - self.prevDist
            self.speed = (self.distTravelled / 5)
            self.prevDist = self.currentDist
            self.distTravelled = 0

    def start(self):
        self.__alarm = Timer.Alarm(self._seconds_handler, 1, periodic=True)
