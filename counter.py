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
