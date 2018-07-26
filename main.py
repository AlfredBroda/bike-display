import os
import time
import utime
import machine
import dht
import ssd1306
import mwifi
import mntptime
import statistics


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
    time_text = "%4d-%02d-%02d %02d:%02d" % (lt[0], lt[1], lt[2], lt[3], lt[4])
    print(time_text)
    oled.text(time_text, 0, line)
    oled.show()


def main():
    old_temp = sens.temperature()
    old_hum = sens.humidity()

    oled.fill(0)
    print("Measuring temp/humidity...")
    try:
        sens.measure()
        temp = sens.temperature()
        hum = sens.humidity()

        stats.collect(temp, hum, utime.localtime()[2])

        if old_temp != temp:
            temp_text = "Temp: %2.1f %+2.1f" % (temp, temp - old_temp)
        else:
            temp_text = "Temp: %2.1f" % temp
        print(temp_text)
        oled.text(temp_text, 0, 20)

        if old_hum != hum:
            hum_text = "Hum: %2.1f %+2.1f" % (hum, hum - old_hum)
        else:
            hum_text = "Hum: %2.1f" % hum
        print(hum_text)
        oled.text(hum_text, 0, 30)
        oled.show()
    except Exception as e:
        print(e)

    wifi.reconnect()
    if wifi.connected():
        mntptime.settime()

    display_wifi()
    display_time()


# This is pin D3 on D-duino
sens = dht.DHT22(machine.Pin(0))
try:
    sens.measure()
except Exception as e:
    print(e)

stats = statistics.TempStats(sens.temperature(), sens.humidity(), utime.localtime()[2])

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
