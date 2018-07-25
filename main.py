import os
import time
import utime
import machine
import dht
import ssd1306
import mwifi
import mntptime


def display_id(line=0):
    os_id = os.uname()
    oled.text('uPython %s' % os_id.version, 0, line)
    oled.text(os_id.machine, 0, line + 10)
    oled.show()


def display_wifi(line=50):
    oled.text(wifi.ip(), 0, line)
    oled.show()


def display_time(line=0):
    lt = utime.localtime()
    oled.text("%4d-%02d-%02d %02d:%02d" % (lt[0], lt[1], lt[2], lt[3], lt[4]), 0, line)
    oled.show()


# This is pin D0 on D-duino
sens = dht.DHT22(machine.Pin(16))
try:
    sens.measure()
except Exception as e:
    print(e)

oldTemp = sens.temperature()
oldHum = sens.humidity()

# These are pins for built in OLED on D-duino
i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)

display_id()

wifi = mwifi.WiFi('example', 'wifi')
try:
    pass_file = open('wifi.txt')
    ssid = pass_file.readline().rstrip('\n')
    pwd = pass_file.readline().rstrip('\n')
    wifi = mwifi.WiFi(ssid, pwd)
    oled.text("WiFi config OK.", 0, 60)
    oled.show()
    wifi.reconnect()
    if wifi.connected():
        mntptime.settime()
except Exception as e:
    print(e)

display_wifi()
display_time(40)

time.sleep(5)

while True:
    sens.measure()
    temp = sens.temperature()
    hum = sens.humidity()

    oled.fill(0)
    display_time()

    if oldTemp != temp:
        oled.text("Temp: %2.1f %+2.1f" % (temp, temp - oldTemp), 0, 20)
    else:
        oled.text("Temp: %2.1f" % temp, 0, 20)
    if oldHum != hum:
        oled.text("Temp: %2.1f %+2.1f" % (hum, hum - oldHum), 0, 30)
    else:
        oled.text("Hum: %2.1f" % hum, 0, 30)
    oldTemp = temp
    oldHum = hum

    display_wifi()
    time.sleep(60)
