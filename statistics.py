def get_min_max(latest, min_old, max_old):
    return min(latest, min_old), max(latest, max_old)


class TempStats:
    def __init__(self, temperature, humidity, day):
        self.temp = temperature
        self.hum = humidity
        self.day = day

        self.max_temp = temperature
        self.min_temp = temperature

        self.max_hum = humidity
        self.min_hum = humidity

    def collect(self, temp, hum, day):
        if day != self.day:
            self.min_temp = temp
            self.min_hum = hum
            self.day = day
        else:
            self.min_hum, self.max_hum = get_min_max(hum, self.min_hum, self.max_hum)
            self.min_temp, self.max_temp = get_min_max(temp, self.min_temp, self.max_temp)
