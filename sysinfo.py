#!/usr/bin/env python3
import sys
import subprocess
from time import sleep
import pifacecad

UPDATE_INTERVAL = 5
GET_IP_CMD = "hostname --all-ip-addresses"
GET_LOADAVG_CMD = "cat /proc/loadavg"
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
USED_MEM_CMD = "free | grep '\-\/+' | awk '{print $3}'"

network_symbol = pifacecad.LCDBitmap([14,14,14,4,4,4,31,0])
load_symbol = pifacecad.LCDBitmap([0,2,7,15,31,31,31,0])
temperature_symbol = pifacecad.LCDBitmap([4,4,4,4,14,14,14,0])
degree_symbol = pifacecad.LCDBitmap([6,9,9,6,0,0,0,0])
memory_symbol = pifacecad.LCDBitmap([14,31,14,31,14,31,14,0])

allow_write = True
display_on = True

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_my_ip():
    val = run_cmd(GET_IP_CMD)[:-1]
    if val == "":
        val = "No Connection!"
    return val

def get_my_load():
    return run_cmd(GET_LOADAVG_CMD)[:-1]

def get_my_temp():
    return run_cmd(GET_TEMP_CMD)[5:9]

def get_my_free_mem():
    total_mem = int(run_cmd(TOTAL_MEM_CMD))
    used_mem = int(run_cmd(USED_MEM_CMD))
    mem_perc = used_mem / total_mem
    return "{:.1%}".format(mem_perc)

def write_load():
    global allow_write

    if allow_write:
        allow_write = False

        cad.lcd.set_cursor(0, 0)

        cad.lcd.write_custom_bitmap(1)
        cad.lcd.write(":{}\n".format(get_my_load()))

        allow_write = True

def write_ip(event):
    global allow_write

    if allow_write:
        allow_write = False

        cad.lcd.set_cursor(0, 0)

        cad.lcd.write_custom_bitmap(0)
        cad.lcd.write(":{}\n".format(get_my_ip()))

        sleep(3)
        allow_write = True
        write_load()

def write_temp_mem():
    global allow_write

    if allow_write:
        allow_write = False

        cad.lcd.set_cursor(0, 1)

        cad.lcd.write_custom_bitmap(2)
        cad.lcd.write(":{}".format(get_my_temp()))
        cad.lcd.write_custom_bitmap(3)
        cad.lcd.write("C ")

        cad.lcd.write_custom_bitmap(4)
        cad.lcd.write(":{}".format(get_my_free_mem()))

        allow_write = True

def start_sysinfo():
    while True:
        if display_on:
            write_load()
            write_temp_mem()

        sleep(UPDATE_INTERVAL)

def display_on_off(event):
    global display_on

    if display_on:
        display_on = False
        cad.lcd.clear()
        cad.lcd.display_off()
        cad.lcd.backlight_off()
    else:
        cad.lcd.display_on()
        cad.lcd.backlight_on()
        display_on = True

        write_load()
        write_temp_mem()

if __name__ == "__main__":
    cad = pifacecad.PiFaceCAD()

    listener = pifacecad.SwitchEventListener()
    listener.register(0, pifacecad.IODIR_ON, write_ip)
    listener.register(4, pifacecad.IODIR_ON, display_on_off)
    listener.activate()

    cad.lcd.blink_off()
    cad.lcd.cursor_off()
    cad.lcd.backlight_on()

    cad.lcd.store_custom_bitmap(0, network_symbol)
    cad.lcd.store_custom_bitmap(1, load_symbol)
    cad.lcd.store_custom_bitmap(2, temperature_symbol)
    cad.lcd.store_custom_bitmap(3, degree_symbol)
    cad.lcd.store_custom_bitmap(4, memory_symbol)

    start_sysinfo()