# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import gc
import webrepl
# import webrepl_setup

esp.osdebug(None)

# webrepl_setup()
webrepl.start()
gc.collect()

