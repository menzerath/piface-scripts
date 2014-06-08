#!/usr/bin/env python3
import sys
import subprocess
from time import sleep
import pifacecad

UPDATE_INTERVAL = 30
URL = "http://menzerath.eu"
GET_STATUS_CMD = "java -jar IMWD.jar " + URL + " --once"

ok_icon = pifacecad.LCDBitmap([0,1,3,22,28,8,0,0])
bad_icon = pifacecad.LCDBitmap([0,27,14,4,14,27,0,0])
url_icon = pifacecad.LCDBitmap([0,8,12,14,12,8,0,0])

prev_status = ""

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_status():
    return run_cmd(GET_STATUS_CMD)[:-1]

def start_testing():
    global prev_status

    while True:
        my_status = get_status()

        if not my_status == prev_status:
            cad.lcd.clear()
            if my_status == "OK":
                cad.lcd.write_custom_bitmap(0)
                cad.lcd.write(" Everything OK")
                cad.lcd.backlight_off()
            else:
                cad.lcd.write_custom_bitmap(1)
                cad.lcd.write(" " + my_status)
                cad.lcd.backlight_on()

            cad.lcd.set_cursor(0, 1)
            cad.lcd.write_custom_bitmap(2)
            cad.lcd.write(" " + URL.replace("http://", "").replace("https://", ""))

        prev_status = my_status
        sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    cad = pifacecad.PiFaceCAD()
    cad.lcd.clear()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()
    cad.lcd.backlight_on()

    cad.lcd.store_custom_bitmap(0, ok_icon)
    cad.lcd.store_custom_bitmap(1, bad_icon)
    cad.lcd.store_custom_bitmap(2, url_icon)

    cad.lcd.write("Starting IMWD...")
    cad.lcd.set_cursor(0, 1)
    cad.lcd.write_custom_bitmap(2)
    cad.lcd.write(" " + URL.replace("http://", "").replace("https://", ""))

    start_testing()