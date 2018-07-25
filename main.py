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


def main():
    old_temp = sens.temperature()
    old_hum = sens.humidity()

    print("Measuring temp/humidity...")
    sens.measure()
    temp = sens.temperature()
    hum = sens.humidity()

    oled.fill(0)
    if old_temp != temp:
        oled.text("Temp: %2.1f %+2.1f" % (temp, temp - old_temp), 0, 20)
    else:
        oled.text("Temp: %2.1f" % temp, 0, 20)
    if old_hum != hum:
        oled.text("Temp: %2.1f %+2.1f" % (hum, hum - old_hum), 0, 30)
    else:
        oled.text("Hum: %2.1f" % hum, 0, 30)
    oled.show()

    wifi.reconnect()
    if wifi.connected():
        mntptime.settime()

    display_wifi()
    display_time()


# This is pin D0 on D-duino
# TODO: Free GPIO16 for use by DeepSleep timer
sens = dht.DHT22(machine.Pin(16))
try:
    sens.measure()
except Exception as e:
    print(e)

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
    oled.text("WiFi config OK.", 0, 30)
    oled.show()
    wifi.reconnect()
except Exception as e:
    print(e)

display_wifi(40)
display_time(50)

time.sleep(5)

tim = machine.Timer(-1)
tim.init(period=60000, mode=machine.Timer.PERIODIC, callback=lambda t: main())

main()
