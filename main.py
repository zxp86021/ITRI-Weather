#!/usr/bin/python
import sys
import time
import serial
import json
import math
import pigpio
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import DHT22
import pmsA003
import LED

"""
GPIO 17 PM2.5 strip Red
GPIO 22 PM2.5 strip Blue
GPIO 27 PM2.5 strip Green
GPIO 5 PM2.5 Level1
GPIO 6 PM2,5 Level2
GPIO 13 PM2.5 Level3
GPIO 19 PM2.5 Level4
GPIO 26 PM2.5 Level5
GPIO 12 PM2.5 Level6

GPIO 11 UV_CLOCK
GPIO 10 UV_DOUT
GPIO 21 temperature_CLOCK
GPIO 20 temperature_DOUT
"""


def int16bit(b):
    return (ord(b[0]) << 8) + ord(b[1])


arduino = serial.Serial('/dev/ttyACM0', 9600)

pi = pigpio.pi()

led = LED.light(pi)

led.all_off()

pm25 = pmsA003.sensor('/dev/ttyUSB0')

dht = DHT22.sensor(pi, 4)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
while True:
    try:
        dht.trigger()

        time.sleep(0.2)

        temperature = dht.temperature()

        humidity = dht.humidity()

        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

        ehPa = (humidity / 100) * 6.105 * math.exp((17.27 * temperature) / (237.7 + temperature))

        pm25_data = pm25.read_data()

        print(pm25_data)

        led.pm25_show(pm25_data['pm2.5'])

        try:
            arduino.reset_input_buffer()
            time.sleep(0.2)
            arduino_json_raw = arduino.readline()
            arduino_json = json.loads(arduino_json_raw)
            print(arduino_json_raw)

            time.sleep(0.2)
            
            uvIndex = ((arduino_json['UV_voltage'] / 5) * 3.3) / 0.1

            print('uvIndex: ' + repr(uvIndex))

            led.uv_show(uvIndex)

            time.sleep(0.2)

            body_temperature = 1.04 * temperature + 0.2 * ehPa - 0.65 * arduino_json['avg_wind_speed'] - 2.7

            print('body_temperature: ' + repr(body_temperature))

            led.body_temperature_show(body_temperature)
        except:
            print('Failed to get arduino reading')

        time.sleep(5)
    except KeyboardInterrupt:
        led.all_off()
        arduino.close()
        dht.cancel()
        pi.stop()
        sys.exit(1)
