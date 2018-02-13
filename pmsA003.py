#!/usr/bin/env python

import serial

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

    def vertify_data(self):
        if not self.data:
            return False
        return True

    def read_data(self):
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
                for c in readBuffer[0:28]: checksum += c
                if checksum != data[self.PMS_CHECKSUM]:
                    print("Incorrect check code: received : {:04x}, calculated : {:04x}".format(data[self.PMS_CHECKSUM]
                                                                                                , checksum))

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

                readEnd = True
                break
        """
        while True:
            b = self.serial.read(1)
            if b == b'\x42':
                data = self.serial.read(31)
                if data[0] == b'\x4d':
                    self.data = bytearray(b'\x42' + data)
                    if self.vertify_data():
                        return self._PMdata()
        """

        """
        self.data = b''
        while True:
            ch1 = self.serial.read()
            if ch1 == b'\x42':
                ch2 = self.serial.read()
                if ch2 == b'\x4d':
                    self.data += ch1 + ch2
                    self.data += self.serial.read(28)
                    if self.vertify_data():
                        return self._PMdata()
        """

    def _PMdata(self):
        d = {}
        d['apm10'] = self.data[4] * 256 + self.data[5]
        d['apm25'] = self.data[6] * 256 + self.data[7]
        d['apm100'] = self.data[8] * 256 + self.data[9]
        d['pm10'] = self.data[10] * 256 + self.data[11],
        d['pm25'] = self.data[12] * 256 + self.data[13],
        d['pm100'] = self.data[14] * 256 + self.data[15],
        d['gt03um'] = self.data[16] * 256 + self.data[17],
        d['gt05um'] = self.data[18] * 256 + self.data[19],
        d['gt10um'] = self.data[20] * 256 + self.data[21],
        d['gt25um'] = self.data[22] * 256 + self.data[23],
        d['gt50um'] = self.data[24] * 256 + self.data[25],
        d['gt100um'] = self.data[26] * 256 + self.data[27]
        return d


import serial
import time
import struct


class PMSA003:
    # constants
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

    def __init__(self, resetPin=17, setPin=18):
        # defining GPIO for RESET line and SET line
        self.resetPin = resetPin
        self.setPin = setPin
        # opening serial port
        self.device = serial.Serial(port	= '/dev/ttyAMA0',
                                    baudrate	= 9600,
                                    stopbits	= serial.STOPBITS_ONE,
                                    parity		= serial.PARITY_NONE,
                                    bytesize	= serial.EIGHTBITS,
                                    timeout		= 5
                                    )
        if not self.device.isOpen(): raise IOError("Unable to open serial")
        # open connection to pigpio
        self.pi = pigpio.pi()
        if not self.pi.connected: raise IOError("Unable to connect to PiGPIOd")

    def getLastReading(self):
        # get last sensor reading
        # flushing input buffer if it's bigger than one reading because i want last reading
        if self.device.in_waiting > 32:
            self.device.reset_input_buffer()

        readEnd = False
        while readEnd is not True:
            while True:
                # checking start frame: 0x42 and 0x4D
                firstByte = self.device.read(1)
                if len(firstByte) < 1 or ord(firstByte) != 0x42: break
                secondByte = self.device.read(1)
                if len(secondByte) < 1 or ord(secondByte) != 0x4D: break

                # reading all the rest!
                readBuffer = self.device.read(30)
                if len(readBuffer) < 30: break

                # decoding data
                data = struct.unpack('!HHHHHHHHHHHHHBBH', readBuffer)

                # checking checksum
                checksum = 0x42 + 0x4D
                for c in readBuffer[0:28]: checksum += c
                if checksum != data[self.PMS_CHECKSUM]:
                    print("Incorrect check code: received : {:04x}, calculated : {:04x}".format(data[self.PMS_CHECKSUM]
                                                                                                ,checksum))

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

                readEnd = True
                break

    def setSleepMode (self, sleepMode):
        # set sensor sleep mode - SETPIN
        if sleepMode is True:
            self.pi.write(self.setPin, 0)
        else:
            self.pi.write(self.setPin, 1)
            # need to wait some time to get proper readings
            time.sleep(self.PMS_WAIT_TIME)

    def setStandbyMode (self, standbyMode):
        # set sensor standby mode - SERIAL
        # command is built as: 0x42 0x4d 0xe4 0x00 0x00/01 checksum
        # standbyMode TRUE sets standby
        if standbyMode is True:
            checksum = 0x4 2 +0x4 D +0xE 4 +0x0 0 +0x00
            serCmd = struct.pack('!BBBBBH' ,0x42 ,0x4D ,0xE4 ,0x00 ,0x00 ,checksum)
            self.device.write(serCmd)
            self.device.reset_input_buffer()
            # checking response: 42 4D 00 04 E4 00 chckH chckL
            response = self.device.read(8)
            if len(response) < 8: print("Response error")
            expected = bytes([0x42 ,0x4D ,0x00 ,0x04 ,0xE4 ,0x00 ,0x01 ,0x77])
            i f(response != expected):
                print("Wrong response received: {} - expected {}".format(response ,expected))
            else:
                print("Standby set")
        else:
            checksum = 0x4 2 +0x4 D +0xE 4 +0x0 0 +0x01
            serCmd = struct.pack('!BBBBBH' ,0x42 ,0x4D ,0xE4 ,0x00 ,0x01 ,checksum)
            self.device.write(serCmd)
            self.device.reset_input_buffer()
            # no answer expected
            # need to wait some time to get proper readings
            time.sleep(self.PMS_WAIT_TIME)
            print("Standby removed")

    def setActiveMode (self, active):
        # set sensor state - SERIAL
        # command is built as: 0x42 0x4d 0xe1 0x00 0x00/01 checksum
        # active TRUE sets active mode
        if active is True:
            checksum = 0x4 2 +0x4 D +0xE 1 +0x0 0 +0x01
            serCmd = struct.pack('!BBBBBH' ,0x42 ,0x4D ,0xE1 ,0x00 ,0x01 ,checksum)
            self.device.write(serCmd)
            self.device.reset_input_buffer()
            # no answer expected
            print("Active mode set")
        else:
            checksum = 0x4 2 +0x4 D +0xE 1 +0x0 0 +0x00
            serCmd = struct.pack('!BBBBBH' ,0x42 ,0x4D ,0xE1 ,0x00 ,0x00 ,checksum)
            self.device.write(serCmd)
            self.device.reset_input_buffer()
            # checking response: 42 4D 00 04 E1 00 1 74
            response = self.device.read(8)
            if len(response) < 8: print("Response error")
            expected = bytes([0x42 ,0x4D ,0x00 ,0x04 ,0xE1 ,0x00 ,0x01 ,0x74])
            i f(response != expected):
                print("Wrong response received: {} - expected {}".format(response ,expected))
            else:
                print("Passive mode set")
            # in passive mode i expect to have single readings, so i'm trashing all the input buffer
            self.device.reset_input_buffer()

    def getSingleReading(self):
        # trigger single reading on passive mode
        checksum = 0x4 2 +0x4 D +0xe 2 +0x0 0 +0x00
        serCmd = struct.pack('!BBBBBH' ,0x42 ,0x4D ,0xE2 ,0x00 ,0x00 ,checksum)
        self.device.write(serCmd)
        self.getLastReading()

    def reset (self):
        # reset sensor - RESETPIN
        self.pi.write(self.resetPin, 0)
        time.sleep(0.5)
        self.pi.write(self.resetPin, 1)

    def close(self):
        ''' Close the serial port.'''
        self.device.close()
        self.pi.stop()

if __name__ == "__main__":

    sensor = PMSA003()

    # print("Setting passive")
    # sensor.setActiveMode(False)
    # time.sleep(1)
    print("Setting active")
    sensor.setActiveMode(True)
    time.sleep(1)
    # print("Setting standby")
    # sensor.setStandbyMode(True)
    # time.sleep(1)
    # print("Removing standby")
    # sensor.setStandbyMode(False)
    # time.sleep(1)

    sensor.getLastReading()
    time.sleep(1)
    sensor.getLastReading()

    # sensor.getSingleReading()
    # time.sleep(1)
    # sensor.getSingleReading()

    sensor.close()

