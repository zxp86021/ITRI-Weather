#!/usr/bin/python
import sys
import time
import serial
import json
import binascii

import Adafruit_DHT

humidity, temperature = Adafruit_DHT.read_retry(22, 4)
arduino = serial.Serial('/dev/ttyACM0', 9600)

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


# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
while True:
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get DHT reading')

    try:
        arduino_json_raw = arduino.readline()
        arduino_json = json.loads(arduino_json_raw)
        print(arduino_json_raw)
    except:
        print('Failed to get arduino reading')

    con = pmsA003('/dev/ttyUSB0')
    d = con.read_data()
    print(d)

    time.sleep(2)
