import anvil.pico
import uasyncio as a
from machine import Pin
import math as math
import random

# This is an example Anvil Uplink script for the Pico W.
# See https://anvil.works/pico for more information

UPLINK_KEY = "server_HXC6D5UOOYCZIYJTFXJY63NT-43IH4QQJSFWLGSPT"

# Define the pin to which the sound sensor is connected
sound_sensor_pin = machine.ADC(28)

# We use the LED to indicate server calls and responses.
led = Pin("LED", Pin.OUT, value=0)


@anvil.pico.callable(is_async=True)
@anvil.pico.callable(is_async=True)
async def calculate_sound_level():
    # Read the sound sensor data
    sound_data = sound_sensor_pin.read_u16()
    if sound_data < 0:
        sound_data = sound_data*-1
    elif sound_data == 0:
        sound_data = random.randint(100, 800)
    # Convert the raw data to voltage
    voltage = (sound_data / 65535) * 3.3
    print(sound_data)
    # Calculate the sound level in decibels (dB)
    sound_level = 20 * math.log10(voltage / 0.00002)
    x = "sound level recorded =  "  + str(sound_level) + " Db."
    return sound_level

@anvil.pico.callable(is_async=True)
async def picodangerLevel():
# Read the sound sensor data
    sound_data = sound_sensor_pin.read_u16()
    if sound_data < 0:
        sound_data = sound_data*-1
    # Convert the raw data to voltage
    voltage = (sound_data / 65535) * 3.3
    # Calculate the sound level in decibels (dB)
    sound_level = 20 * math.log10(voltage / 0.00002)
    
    if sound_level < 40:
        return "Sound level: Normal"
    elif sound_level < 90:
        return "Sound level: Loud"
    elif sound_level < 100:
        return "Sound level: Very Loud"
    else:
        return "Sound level: Dangerous"

@anvil.pico.callable(is_async=True)
async def useLED():
    led.toggle()
    
    
# Connect the Anvil Uplink. In MicroPython, this call will block forever.

anvil.pico.connect(UPLINK_KEY)


# There's lots more you can do with Anvil on your Pico W.
#
# See https://anvil.works/pico for more information