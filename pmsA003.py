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

    def vertify_data(self):
        if not self.data:
            return False
        return True

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

                readEnd = True
                break
        """
        while True:
            b = self.serial.read(1)
            if b == b'\x42':
                data = self.serial.read(31)
                if data[0] == b'\x4d':
                    self.data = b'\x42' + data
                    if self.vertify_data():
                        return self._PMdata()
        """
        """
        frame = b''
        while True:
            b0 = self.serial.read()
            if b0 == b'\x42':
                b1 = self.serial.read()
                if b1 == b'\x4d':
                    b2 = self.serial.read()
                    b3 = self.serial.read()
                    frame_len = ord(b2) * 256 + ord(b3)
                    if frame_len == DATA_FRAME_LENGTH:
                        # Normal data frame.
                        frame += b0 + b1 + b2 + b3
                        frame += self.serial.read(frame_len)
                        if (len(frame) - 4) != frame_len:
                            return None
                        # Verify checksum (last two bytes).
                        expected = self.int16bit(frame[-2:])
                        checksum = 0
                        for i in range(0, len(frame) - 2):
                            checksum += ord(frame[i])
                        if checksum != expected:
                            return None
                        return frame
                    elif frame_len == CMD_FRAME_LENGTH:
                        # Command response frame.
                        frame += b0 + b1 + b2 + b3
                        frame += self.serial.read(frame_len)
                        return frame
                    else:
                        # Unexpected frame.
                        logging.error("Unexpected frame length = %d" % (frame_len))
                        time.sleep(MAX_TOTAL_RESPONSE_TIME)
                        self.serial.reset_input_buffer()
                        return None

                    self.data += ch1 + ch2
                    self.data += self.serial.read(28)
                    if self.vertify_data():
                        return self._PMdata()

                    """

    def _PMdata(self):
        d = {}
        """
        pm1_cf = int(data_hex[4] + data_hex[5] + data_hex[6] + data_hex[7], 16)
        pm25_cf = int(data_hex[8] + data_hex[9] + data_hex[10] + data_hex[11], 16)
        pm10_cf = int(data_hex[12] + data_hex[13] + data_hex[14] + data_hex[15], 16)
        pm1 = int(data_hex[16] + data_hex[17] + data_hex[18] + data_hex[19], 16)
        pm25 = int(data_hex[20] + data_hex[21] + data_hex[22] + data_hex[23], 16)
        pm10 = int(data_hex[24] + data_hex[25] + data_hex[26] + data_hex[27], 16)
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
        
        int16bit(rcv[4:]),
        'data2':     int16bit(rcv[6:]),
        'data3':     int16bit(rcv[8:]),
        'data4':     int16bit(rcv[10:]),
        'data5':     int16bit(rcv[12:]),
        'data6':     int16bit(rcv[14:]),
        'data7':     int16bit(rcv[16:]),
        'data8':     int16bit(rcv[18:]),
        'data9':     int16bit(rcv[20:]),
        'data10':    int16bit(rcv[22:]),
        'data11':    int16bit(rcv[24:]),
        'data12':    int16bit(rcv[26:]),
        'reserved':  buff2hex(rcv[28:30]),
        'checksum': int16bit(rcv[30:])
        """
        """
        d['apm10'] = self.int16bit(self.data[4:]),
        d['apm25'] = self.int16bit(self.data[6:]),
        d['apm100'] = self.int16bit(self.data[8:]),
        d['pm10'] = self.int16bit(self.data[10:]),
        d['pm25'] = self.int16bit(self.data[12:]),
        d['pm100'] = self.int16bit(self.data[14:]),
        """

        d['apm10'] = self.data[4:],
        d['apm25'] = self.data[6:],
        d['apm100'] = self.data[8:],
        d['pm10'] = self.data[10:],
        d['pm25'] = self.data[12:],
        d['pm100'] = self.data[14:],

        return d
