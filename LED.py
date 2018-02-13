#!/usr/bin/env python

import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

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

class light:
    def __init__(self, pi):
        self.pi = pi

        # Configure the count of pixels:
        self.PIXEL_COUNT = 32

        self.UV_CLOCK = 11
        self.UV_DOUT = 10
        self.temperature_CLOCK = 21
        self.temperature_DOUT = 20

        # UV indicator
        self.UV_pixels = Adafruit_WS2801.WS2801Pixels(self.PIXEL_COUNT, clk=self.UV_CLOCK, do=self.UV_DOUT)

        # temperature indicator
        self.temperature_pixels = Adafruit_WS2801.WS2801Pixels(self.PIXEL_COUNT,
                                                               clk=self.temperature_CLOCK,
                                                               do=self.temperature_DOUT)

        """
        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        self.UV_SPI_PORT = 0
        self.UV_SPI_DEVICE = 0
        self.UV_pixels = Adafruit_WS2801.WS2801Pixels(self.PIXEL_COUNT,
                                                      spi=SPI.SpiDev(self.UV_SPI_PORT, self.UV_SPI_DEVICE))

        self.temperature_SPI_PORT = 0
        self.temperature_SPI_DEVICE = 1
        self.temperature_pixels = Adafruit_WS2801.WS2801Pixels(self.PIXEL_COUNT,
                                                               spi=SPI.SpiDev(self.temperature_SPI_PORT,
                                                                              self.temperature_SPI_DEVICE))
        """

        # level 1 ~ level 6 pin number
        self.pm25_level = [5, 6, 13, 19, 26, 12]

        self.pm25_RGB_R = 17
        self.pm25_RGB_G = 27
        self.pm25_RGB_B = 22

    def all_off(self):
        for pin in self.pm25_level:
            self.pi.write(pin, 0)

        self.pi.set_PWM_dutycycle(self.pm25_RGB_R, 0)
        self.pi.set_PWM_dutycycle(self.pm25_RGB_G, 0)
        self.pi.set_PWM_dutycycle(self.pm25_RGB_B, 0)

        # Clear ws2801 all the pixels to turn them off.
        self.UV_pixels.clear()
        self.UV_pixels.show()  # Make sure to call show() after changing any pixels!

        self.temperature_pixels.clear()
        self.temperature_pixels.show()  # Make sure to call show() after changing any pixels!

    def pm25_show(self, read_value):
        if read_value <= 50:
            self.pi.set_PWM_dutycycle(self.pm25_RGB_R, 0)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_G, 255)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_B, 0)
            level = 1
            self.pi.write(5, 1)
            self.pi.write(6, 0)
            self.pi.write(13, 0)
            self.pi.write(19, 0)
            self.pi.write(26, 0)
            self.pi.write(12, 0)
        elif 50 < read_value <= 100:
            self.pi.set_PWM_dutycycle(self.pm25_RGB_R, 255)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_G, 128)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_B, 0)
            level = 2
            self.pi.write(5, 1)
            self.pi.write(6, 1)
            self.pi.write(13, 0)
            self.pi.write(19, 0)
            self.pi.write(26, 0)
            self.pi.write(12, 0)
        elif 100 < read_value <= 150:
            self.pi.set_PWM_dutycycle(self.pm25_RGB_R, 255)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_G, 25)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_B, 0)
            level = 3
            self.pi.write(5, 1)
            self.pi.write(6, 1)
            self.pi.write(13, 1)
            self.pi.write(19, 0)
            self.pi.write(26, 0)
            self.pi.write(12, 0)
        elif 150 < read_value <= 200:
            self.pi.set_PWM_dutycycle(self.pm25_RGB_R, 255)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_G, 0)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_B, 0)
            level = 4
            self.pi.write(5, 1)
            self.pi.write(6, 1)
            self.pi.write(13, 1)
            self.pi.write(19, 1)
            self.pi.write(26, 0)
            self.pi.write(12, 0)
        elif 200 < read_value <= 300:
            self.pi.set_PWM_dutycycle(self.pm25_RGB_R, 160)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_G, 0)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_B, 240)
            level = 5
            self.pi.write(5, 1)
            self.pi.write(6, 1)
            self.pi.write(13, 1)
            self.pi.write(19, 1)
            self.pi.write(26, 1)
            self.pi.write(12, 0)
        else:
            self.pi.set_PWM_dutycycle(self.pm25_RGB_R, 70)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_G, 20)
            self.pi.set_PWM_dutycycle(self.pm25_RGB_B, 10)
            level = 6
            self.pi.write(5, 1)
            self.pi.write(6, 1)
            self.pi.write(13, 1)
            self.pi.write(19, 1)
            self.pi.write(26, 1)
            self.pi.write(12, 1)

    def uv_show(self, read_value):
        if read_value < 3:
            self.UV_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.UV_pixels.set_pixel_rgb(i, 26, 13, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.UV_pixels.set_pixel_rgb(i, 26, 7, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.UV_pixels.set_pixel_rgb(i, 26, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.UV_pixels.set_pixel_rgb(i, 16, 0, 24)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.UV_pixels.set_pixel_rgb(i, 255, 25, 0)

            #for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.UV_pixels.show()
        elif read_value < 6:
            self.UV_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.UV_pixels.set_pixel_rgb(i, 255, 128, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.UV_pixels.set_pixel_rgb(i, 26, 7, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.UV_pixels.set_pixel_rgb(i, 26, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.UV_pixels.set_pixel_rgb(i, 16, 0, 24)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.UV_pixels.set_pixel_rgb(i, 255, 25, 0)

            #for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.UV_pixels.show()
        elif read_value < 8:
            self.UV_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.UV_pixels.set_pixel_rgb(i, 255, 128, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.UV_pixels.set_pixel_rgb(i, 255, 25, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.UV_pixels.set_pixel_rgb(i, 26, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.UV_pixels.set_pixel_rgb(i, 16, 0, 24)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.UV_pixels.set_pixel_rgb(i, 255, 25, 0)

            #for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.UV_pixels.show()
        elif read_value < 11:
            self.UV_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.UV_pixels.set_pixel_rgb(i, 255, 128, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.UV_pixels.set_pixel_rgb(i, 255, 25, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.UV_pixels.set_pixel_rgb(i, 255, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.UV_pixels.set_pixel_rgb(i, 16, 0, 24)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.UV_pixels.set_pixel_rgb(i, 255, 25, 0)

            for i in range(self.PIXEL_COUNT):
                print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.UV_pixels.show()
        else:
            self.UV_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.UV_pixels.set_pixel_rgb(i, 0, 255, 0)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.UV_pixels.set_pixel_rgb(i, 255, 128, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.UV_pixels.set_pixel_rgb(i, 255, 25, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.UV_pixels.set_pixel_rgb(i, 255, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.UV_pixels.set_pixel_rgb(i, 160, 0, 240)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.UV_pixels.set_pixel_rgb(i, 255, 25, 0)

            #for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.UV_pixels.show()

    def body_temperature_show(self, read_value):
        if read_value <= 10:
            self.temperature_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.temperature_pixels.set_pixel_rgb(i, 16, 0, 24)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.temperature_pixels.set_pixel_rgb(i, 26, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.temperature_pixels.set_pixel_rgb(i, 26, 13, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.temperature_pixels.set_pixel_rgb(i, 0, 26, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.temperature_pixels.set_pixel_rgb(i, 0, 0, 255)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.temperature_pixels.set_pixel_rgb(i, 255, 25, 0)

            # for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.temperature_pixels.show()
        elif 10 < read_value <= 20:
            self.temperature_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.temperature_pixels.set_pixel_rgb(i, 16, 0, 24)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.temperature_pixels.set_pixel_rgb(i, 26, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.temperature_pixels.set_pixel_rgb(i, 26, 13, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.temperature_pixels.set_pixel_rgb(i, 0, 255, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.temperature_pixels.set_pixel_rgb(i, 0, 0, 255)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.temperature_pixels.set_pixel_rgb(i, 255, 25, 0)

            # for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.temperature_pixels.show()
        elif 20 < read_value <= 27:
            self.temperature_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.temperature_pixels.set_pixel_rgb(i, 16, 0, 24)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.temperature_pixels.set_pixel_rgb(i, 26, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.temperature_pixels.set_pixel_rgb(i, 255, 128, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.temperature_pixels.set_pixel_rgb(i, 0, 255, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.temperature_pixels.set_pixel_rgb(i, 0, 0, 255)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.temperature_pixels.set_pixel_rgb(i, 255, 25, 0)

            # for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.temperature_pixels.show()
        elif 27 < read_value <= 30:
            self.temperature_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.temperature_pixels.set_pixel_rgb(i, 16, 0, 24)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.temperature_pixels.set_pixel_rgb(i, 255, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.temperature_pixels.set_pixel_rgb(i, 255, 128, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.temperature_pixels.set_pixel_rgb(i, 0, 255, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.temperature_pixels.set_pixel_rgb(i, 0, 0, 255)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.temperature_pixels.set_pixel_rgb(i, 255, 25, 0)

            # for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.temperature_pixels.show()
        else:
            self.temperature_pixels.clear()

            for i in range(self.PIXEL_COUNT // 6):
                self.temperature_pixels.set_pixel_rgb(i, 160, 0, 240)  # Set the RGB color (0-255) of pixel i.

            for i in range(self.PIXEL_COUNT // 6, self.PIXEL_COUNT // 6 * 2):
                self.temperature_pixels.set_pixel_rgb(i, 255, 0, 0)

            for i in range(self.PIXEL_COUNT // 6 * 2, self.PIXEL_COUNT // 6 * 3):
                self.temperature_pixels.set_pixel_rgb(i, 255, 128, 0)

            for i in range(self.PIXEL_COUNT // 6 * 3, self.PIXEL_COUNT // 6 * 4):
                self.temperature_pixels.set_pixel_rgb(i, 0, 255, 0)

            for i in range(self.PIXEL_COUNT // 6 * 4, self.PIXEL_COUNT // 6 * 5):
                self.temperature_pixels.set_pixel_rgb(i, 0, 0, 255)

            for i in range(self.PIXEL_COUNT // 6 * 5, self.PIXEL_COUNT):
                self.temperature_pixels.set_pixel_rgb(i, 255, 25, 0)

            # for i in range(self.PIXEL_COUNT):
            #    print(self.UV_pixels.get_pixel_rgb(i))
            # Now make sure to call show() to update the pixels with the colors set above!
            self.temperature_pixels.show()