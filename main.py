#!/usr/bin/python
import sys
import time
import serial
import json
import binascii
import math
import pigpio
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import Adafruit_DHT

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

arduino = serial.Serial('/dev/ttyACM0', 9600)

# Configure the count of pixels:
PIXEL_COUNT = 32

UV_CLOCK = 11
UV_DOUT = 10
temperature_CLOCK = 21
temperature_DOUT = 20

UV_pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=UV_CLOCK, do=UV_DOUT)
temperature_pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=temperature_CLOCK, do=temperature_DOUT)


class pmsA003():
    def __init__(self, dev):
        self.serial = serial.Serial(dev, 9600)
        self.serial.write(b'\x42\x4D\xE4\x00\x01\x01\x74')

    def __exit__(self, exc_type, exc_value, traceback):
        self.serial.close()

    def setIdel(self):
        idelcmd = b'\x42\x4d\xe4\x00\x00\x01\x73'
        ary = bytearray(idelcmd)
        self.serial.write(ary)

    def setNormal(self):
        normalcmd = b'\x42\x4d\xe4\x00\x01\x01\x74'
        ary = bytearray(normalcmd)
        self.serial.write(ary)

    def vertify_data(self):
        if not self.data:
            return False
        return True

    def read_data(self):
        while True:
            b = self.serial.read(1)
            if b == b'\x42':
                data = self.serial.read(31)
                if data[0] == b'\x4d':
                    self.data = bytearray(b'\x42' + data)
                    if self.vertify_data():
                        return self._PMdata()

    def _PMdata(self):
        d = {} 
        d['apm10'] = self.data[4] * 256 + self.data[5]
        d['apm25'] = self.data[6] * 256 + self.data[7]
        d['apm100'] = self.data[8] * 256 + self.data[9]
        """
        d['pm10'] = self.data[10] * 256 + self.data[11],
        d['pm25'] = self.data[12] * 256 + self.data[13],
        d['pm100'] = self.data[14] * 256 + self.data[15],
        d['gt03um'] = self.data[16] * 256 + self.data[17],
        d['gt05um'] = self.data[18] * 256 + self.data[19],
        d['gt10um'] = self.data[20] * 256 + self.data[21],
        d['gt25um'] = self.data[22] * 256 + self.data[23],
        d['gt50um'] = self.data[24] * 256 + self.data[25],
        d['gt100um'] = self.data[26] * 256 + self.data[27]
        """
        return d


def led_init():
    pi_led.set_PWM_dutycycle(17, 0)
    pi_led.set_PWM_dutycycle(22, 0)
    pi_led.set_PWM_dutycycle(27, 0)
    pi_led.write(5, 0)
    pi_led.write(6, 0)
    pi_led.write(13, 0)
    pi_led.write(19, 0)
    pi_led.write(26, 0)
    pi_led.write(12, 0)
    # Clear ws2801 all the pixels to turn them off.
    UV_pixels.clear()
    UV_pixels.show()  # Make sure to call show() after changing any pixels!
    temperature_pixels.clear()
    temperature_pixels.show()  # Make sure to call show() after changing any pixels!


pi_led = pigpio.pi()
led_init()

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
while True:
    try:
        humidity, temperature = Adafruit_DHT.read_retry(22, 4)

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get DHT reading')

        try:
            arduino_json_raw = arduino.readline()
            arduino_json = json.loads(arduino_json_raw)
            print(arduino_json_raw)

            uvIndex = ((arduino_json['UV_voltage'] / 5) * 3.3) / 0.1

            if uvIndex < 3:
                for i in range(PIXEL_COUNT // 6):
                    UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

                for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                    UV_pixels.set_pixel_rgb(i, 255, 25, 0)
                # Now make sure to call show() to update the pixels with the colors set above!
                UV_pixels.show()
            elif uvIndex < 6:
                for i in range(PIXEL_COUNT // 6):
                    UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

                for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                    UV_pixels.set_pixel_rgb(i, 255, 128, 0)

                for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                    UV_pixels.set_pixel_rgb(i, 255, 25, 0)
                # Now make sure to call show() to update the pixels with the colors set above!
                UV_pixels.show()
            elif uvIndex < 8:
                for i in range(PIXEL_COUNT // 6):
                    UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

                for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                    UV_pixels.set_pixel_rgb(i, 255, 128, 0)

                for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                    UV_pixels.set_pixel_rgb(i, 255, 25, 0)

                for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                    UV_pixels.set_pixel_rgb(i, 255, 25, 0)
                # Now make sure to call show() to update the pixels with the colors set above!
                UV_pixels.show()
            elif uvIndex < 11:
                for i in range(PIXEL_COUNT // 6):
                    UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

                for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                    UV_pixels.set_pixel_rgb(i, 255, 128, 0)

                for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                    UV_pixels.set_pixel_rgb(i, 255, 25, 0)

                for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                    UV_pixels.set_pixel_rgb(i, 255, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                    UV_pixels.set_pixel_rgb(i, 0, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                    UV_pixels.set_pixel_rgb(i, 255, 25, 0)
                # Now make sure to call show() to update the pixels with the colors set above!
                UV_pixels.show()
            else:
                for i in range(PIXEL_COUNT // 6):
                    UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

                for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                    UV_pixels.set_pixel_rgb(i, 255, 128, 0)

                for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                    UV_pixels.set_pixel_rgb(i, 255, 25, 0)

                for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                    UV_pixels.set_pixel_rgb(i, 255, 0, 0)

                for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                    UV_pixels.set_pixel_rgb(i, 160, 0, 240)

                for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                    UV_pixels.set_pixel_rgb(i, 255, 25, 0)
                # Now make sure to call show() to update the pixels with the colors set above!
                UV_pixels.show()

            if humidity is not None and temperature is not None:
                ehPa = (humidity / 100) * 6.105 * math.exp((17.27 * temperature) / (237.7 + temperature))
                body_temperature = 1.04 * temperature + 0.2 * ehPa - 0.65 * arduino_json['avg_wind_speed'] - 2.7

                print('body_temperature: ' + repr(body_temperature))

                if body_temperature <= 10:
                    print('body_temperature: <= 10')
                    for i in range(PIXEL_COUNT // 6):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 255)  # Set the RGB color (0-255) of pixel i.

                    for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                        temperature_pixels.set_pixel_rgb(i, 255, 25, 0)
                    # Now make sure to call show() to update the pixels with the colors set above!
                    temperature_pixels.show()
                elif 10 < body_temperature <= 20:
                    print('body_temperatere: 11-20')
                    for i in range(PIXEL_COUNT // 6):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 255)  # Set the RGB color (0-255) of pixel i.

                    for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                        temperature_pixels.set_pixel_rgb(i, 0, 255, 0)

                    for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                        temperature_pixels.set_pixel_rgb(i, 255, 25, 0)
                    # Now make sure to call show() to update the pixels with the colors set above!
                    temperature_pixels.show()
                elif 20 < body_temperature <= 27:
                    print('body_temperature: 21-27')
                    for i in range(PIXEL_COUNT // 6):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 255)  # Set the RGB color (0-255) of pixel i.

                    for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                        temperature_pixels.set_pixel_rgb(i, 0, 255, 0)

                    for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                        temperature_pixels.set_pixel_rgb(i, 255, 128, 0)

                    for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                        temperature_pixels.set_pixel_rgb(i, 255, 25, 0)
                    # Now make sure to call show() to update the pixels with the colors set above!
                    temperature_pixels.show()
                elif 27 < body_temperature <= 30:
                    print('body_temperature: 28-30')
                    for i in range(PIXEL_COUNT // 6):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 255)  # Set the RGB color (0-255) of pixel i.

                    for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                        temperature_pixels.set_pixel_rgb(i, 0, 255, 0)

                    for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                        temperature_pixels.set_pixel_rgb(i, 255, 128, 0)

                    for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                        temperature_pixels.set_pixel_rgb(i, 255, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                        temperature_pixels.set_pixel_rgb(i, 255, 25, 0)
                    # Now make sure to call show() to update the pixels with the colors set above!
                    temperature_pixels.show()
                else:
                    print('body_temperature: 30+')
                    for i in range(PIXEL_COUNT // 6):
                        temperature_pixels.set_pixel_rgb(i, 0, 0, 255)  # Set the RGB color (0-255) of pixel i.

                    for i in range(PIXEL_COUNT // 6, PIXEL_COUNT // 6 * 2):
                        temperature_pixels.set_pixel_rgb(i, 0, 255, 0)

                    for i in range(PIXEL_COUNT // 6 * 2, PIXEL_COUNT // 6 * 3):
                        temperature_pixels.set_pixel_rgb(i, 255, 128, 0)

                    for i in range(PIXEL_COUNT // 6 * 3, PIXEL_COUNT // 6 * 4):
                        temperature_pixels.set_pixel_rgb(i, 255, 0, 0)

                    for i in range(PIXEL_COUNT // 6 * 4, PIXEL_COUNT // 6 * 5):
                        temperature_pixels.set_pixel_rgb(i, 160, 0, 240)

                    for i in range(PIXEL_COUNT // 6 * 5, PIXEL_COUNT):
                        temperature_pixels.set_pixel_rgb(i, 255, 25, 0)
                    # Now make sure to call show() to update the pixels with the colors set above!
                    temperature_pixels.show()
        except:
            print('Failed to get arduino reading')

        con = pmsA003('/dev/ttyUSB0')
        d = con.read_data()
        print('PM2.5: ' + repr(d['apm25']))
        if d['apm25'] <= 50:
            pi_led.set_PWM_dutycycle(17, 0)
            pi_led.set_PWM_dutycycle(22, 0)
            pi_led.set_PWM_dutycycle(27, 255)
            pi_led.write(5, 1)
            pi_led.write(6, 0)
            pi_led.write(13, 0)
            pi_led.write(19, 0)
            pi_led.write(26, 0)
            pi_led.write(12, 0)
        elif 50 < d['apm25'] <= 100:
            pi_led.set_PWM_dutycycle(17, 255)
            pi_led.set_PWM_dutycycle(22, 0)
            pi_led.set_PWM_dutycycle(27, 128)
            pi_led.write(5, 1)
            pi_led.write(6, 1)
            pi_led.write(13, 0)
            pi_led.write(19, 0)
            pi_led.write(26, 0)
            pi_led.write(12, 0)
        elif 100 < d['apm25'] <= 150:
            pi_led.set_PWM_dutycycle(17, 255)
            pi_led.set_PWM_dutycycle(22, 0)
            pi_led.set_PWM_dutycycle(27, 25)
            pi_led.write(5, 1)
            pi_led.write(6, 1)
            pi_led.write(13, 1)
            pi_led.write(19, 0)
            pi_led.write(26, 0)
            pi_led.write(12, 0)
        elif 150 < d['apm25'] <= 200:
            pi_led.set_PWM_dutycycle(17, 255)
            pi_led.set_PWM_dutycycle(22, 0)
            pi_led.set_PWM_dutycycle(27, 0)
            pi_led.write(5, 1)
            pi_led.write(6, 1)
            pi_led.write(13, 1)
            pi_led.write(19, 1)
            pi_led.write(26, 0)
            pi_led.write(12, 0)
        elif 200 < d['apm25'] <= 300:
            pi_led.set_PWM_dutycycle(17, 160)
            pi_led.set_PWM_dutycycle(22, 240)
            pi_led.set_PWM_dutycycle(27, 0)
            pi_led.write(5, 1)
            pi_led.write(6, 1)
            pi_led.write(13, 1)
            pi_led.write(19, 1)
            pi_led.write(26, 1)
            pi_led.write(12, 0)
        else:
            pi_led.set_PWM_dutycycle(17, 70)
            pi_led.set_PWM_dutycycle(22, 10)
            pi_led.set_PWM_dutycycle(27, 20)
            pi_led.write(5, 1)
            pi_led.write(6, 1)
            pi_led.write(13, 1)
            pi_led.write(19, 1)
            pi_led.write(26, 1)
            pi_led.write(12, 1)

        time.sleep(5)

    except KeyboardInterrupt:
        led_init()
        arduino.close()
        sys.exit(1)
