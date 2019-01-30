#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
# Sensor ID
UIDa = "kFD" # Realy
UIDb = "vxS" # Button
UIDc = "Fu2" # Sound Pressure Level

# Tinkerforge 
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button import BrickletDualButton
from tinkerforge.bricklet_dual_relay import BrickletDualRelay
from tinkerforge.bricklet_sound_pressure_level import BrickletSoundPressureLevel

# Sensors
ipcon= IPConnection() # Create IP connection
drelay  = BrickletDualRelay(UIDa, ipcon)
dbutton = BrickletDualButton(UIDb, ipcon)
spl  = BrickletSoundPressureLevel(UIDc, ipcon)


ipcon.connect(HOST, PORT) # Connect to brickd
# Don't use device before ipcon is connected

def switch_on_1(button_l, button_r, led_l, led_r):
    relay1, relay2 = drelay.get_state()
    if relay2 and button_l == dbutton.BUTTON_STATE_RELEASED:
        drelay.set_selected_state(2, False)
        dbutton.set_selected_led_state(0,True)
    elif not relay2 and button_l == dbutton.BUTTON_STATE_RELEASED: 
        drelay.set_selected_state(2,True)
        dbutton.set_selected_led_state(0,False)

def switch_on_2(decibel):
    relay1, relay2 = drelay.get_state()
    if relay2: 
        drelay.set_selected_state(2, False)
        dbutton.set_selected_led_state(0,True)
    else: 
        drelay.set_selected_state(2,True)
        dbutton.set_selected_led_state(0,False)

def off():
    drelay.set_state(False, False)
    dbutton.set_led_state(1,1)  

def exit():
    ipcon.disconnect()

def my_callback(param):
    print(param)

off()

if __name__ == "__main__":
    # Configure threshold for decibel "greater than xx dB(A)"
    db = 85
    
    # with a debounce period of 1s (1000ms)
    spl.set_decibel_callback_configuration(1000, False, ">", db*10, 0)  
    # Register decibel callback to function move
    spl.register_callback(spl.CALLBACK_DECIBEL, switch_on_2)
    
    # Register state changed callback to function cb_state_changed
    dbutton.register_callback(dbutton.CALLBACK_STATE_CHANGED, switch_on_1)




