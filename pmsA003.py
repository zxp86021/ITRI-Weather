#!/usr/bin/env python

import serial
import struct

class sensor:
    PMS_FRAME_LENGTH = 0
    PMS_PM1_0 = 1
    PMS_PM2_5 = 2
    PMS_PM10_0 = 3
    PMS_PM1_0_ATM = 4
    PMS_PM2_5_ATM = 5
    PMS_PM10_0_ATM = 6
    PMS_PCNT_0_3 = 7
    PMS_PCNT_0_5 = 8
    PMS_PCNT_1_0 = 9
    PMS_PCNT_2_5 = 10
    PMS_PCNT_5_0 = 11
    PMS_PCNT_10_0 = 12
    PMS_VERSION = 13
    PMS_ERROR = 14
    PMS_CHECKSUM = 15
    PMS_WAIT_TIME = 30  # time to wait when sensor exits sleep mode

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

    def read_data(self):
        # get last sensor reading
        # flushing input buffer if it's bigger than one reading because i want last reading
        if self.serial.in_waiting > 32:
            self.serial.reset_input_buffer()

        readEnd = False
        while readEnd is not True:
            while True:
                # checking start frame: 0x42 and 0x4D
                firstByte = self.serial.read(1)
                if len(firstByte) < 1 or ord(firstByte) != 0x42: break
                secondByte = self.serial.read(1)
                if len(secondByte) < 1 or ord(secondByte) != 0x4D: break

                # reading all the rest!
                readBuffer = self.serial.read(30)
                if len(readBuffer) < 30: break

                # decoding data
                data = struct.unpack('!HHHHHHHHHHHHHBBH', readBuffer)

                # checking checksum
                checksum = 0x42 + 0x4D
                for c in readBuffer[0:28]: checksum += ord(c)
                if checksum != data[self.PMS_CHECKSUM]:
                    print("Incorrect check code: received : {:04x}, calculated : {:04x}".format(data[self.PMS_CHECKSUM],
                                                                                                checksum))

                # parsing sensor data
                # 0-1: frame length
                print("Frame length: {}".format(data[self.PMS_FRAME_LENGTH]))

                # 2-3: pm1
                print("pm1: {}".format(data[self.PMS_PM1_0]))

                # 4-5: pm2.5
                print("pm2.5: {}".format(data[self.PMS_PM2_5]))

                # 6-7: pm10
                print("pm10: {}".format(data[self.PMS_PM10_0]))

                # 8-9: pm1 atm
                print("pm1 atm: {}".format(data[self.PMS_PM1_0_ATM]))

                # 10-11: pm2.5 atm
                print("pm2.5 atm: {}".format(data[self.PMS_PM2_5_ATM]))

                # 12-13: pm10 atm
                print("pm10 atm: {}".format(data[self.PMS_PM10_0_ATM]))

                # 14-15: pm0.3 count
                print("pm0.3 count: {}".format(data[self.PMS_PCNT_0_3]))

                # 16-17: pm0.5 count
                print("pm0.5 count: {}".format(data[self.PMS_PCNT_0_5]))

                # 18-19: pm1 count
                print("pm1 count: {}".format(data[self.PMS_PCNT_1_0]))

                # 20-21: pm2.5 count
                print("pm2.5 count: {}".format(data[self.PMS_PCNT_2_5]))

                # 22-23: pm5 count
                print("pm5 count: {}".format(data[self.PMS_PCNT_5_0]))

                # 24-25: pm10 count
                print("pm10 count: {}".format(data[self.PMS_PCNT_10_0]))

                # 26: Version
                print("Version: {}".format(data[self.PMS_VERSION]))

                # 27: Error
                print("Error: {}".format(data[self.PMS_ERROR]))

                # 28-29: checksum
                print("Checksum: {}".format(data[self.PMS_CHECKSUM]))

                d = {}
                d['Frame length'] = data[self.PMS_FRAME_LENGTH]
                d['pm1'] = data[self.PMS_PM1_0]
                d['pm2.5'] = data[self.PMS_PM2_5]
                d['pm10'] = data[self.PMS_PM10_0]

                readEnd = True
                break

        return d
