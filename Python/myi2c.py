import smbus
import time
from signal import pause
from gpiozero import LED

class NavioPWM:

    __GPIO_OUT_ENBL = 27

    # Registers/etc.
    __MODE1 = 0x00
    __MODE2 = 0x01
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALL_LED_ON_L = 0xFA
    __ALL_LED_ON_H = 0xFB
    __ALL_LED_OFF_L = 0xFC
    __ALL_LED_OFF_H = 0xFD

    # Bits
    __RESTART = 0x80
    __SLEEP = 0x10
    __ALLCALL = 0x01
    __INVRT = 0x10
    __OUTDRV = 0x04

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x40
        self.pin_enable = LED(self.__GPIO_OUT_ENBL)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels"""
        self.bus.write_byte_data(self.address, self.__ALL_LED_ON_L, on & 0xFF)
        self.bus.write_byte_data(self.address, self.__ALL_LED_ON_H, on >> 8)
        self.bus.write_byte_data(self.address, self.__ALL_LED_OFF_L, off & 0xFF)
        self.bus.write_byte_data(self.address, self.__ALL_LED_OFF_H, off >> 8)

    def set_pwm(self, channel, duty_cycle=0.5, delay=0.0):
        if delay + duty_cycle <= 1:
            on = int(delay*4095)
            off = int(duty_cycle*4095) + on
            self.bus.write_byte_data(self.address, self.__LED0_ON_L + 4 * channel, on & 0xFF)
            self.bus.write_byte_data(self.address, self.__LED0_ON_H + 4 * channel, on >> 8)
            self.bus.write_byte_data(self.address, self.__LED0_OFF_L + 4 * channel, off & 0xFF)
            self.bus.write_byte_data(self.address, self.__LED0_OFF_H + 4 * channel, off >> 8)

    def start(self):
        self.pin_enable.off() # Reversed logic
        self.set_all_pwm(0, 0)
        self.bus.write_byte_data(self.address, self.__MODE2, self.__OUTDRV)
        self.bus.write_byte_data(self.address, self.__MODE1, self.__ALLCALL)
        time.sleep(0.005)  # wait for oscillator
        mode1 = self.bus.read_byte_data(self.address, self.__MODE1)
        mode1 = mode1 & ~self.__SLEEP  # wake up (reset sleep)
        self.bus.write_byte_data(self.address, self.__MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator

class NavioLED:

    __R_CHANNEL = 2
    __G_CHANNEL = 1
    __B_CHANNEL = 0

    RED = (1, 0, 0)
    BLUE = (0, 1, 0)
    GREEN = (0, 0, 1)
    PURPLE = (1, 1, 0)
    YELLOW = (1, 0, 1)
    CYAN = (0, 1, 1)

    def __init__(self):
        self.pwm = NavioPWM()

    def on(self, color=(1.0, 1.0, 1.0), saturation=1.0):
        self.pwm.set_pwm(self.__R_CHANNEL, 1 - color[0]*saturation)
        self.pwm.set_pwm(self.__G_CHANNEL, 1 - color[1]*saturation)
        self.pwm.set_pwm(self.__B_CHANNEL, 1 - color[2]*saturation)

    def off(self):
        self.on((0, 0, 0))

    def pulse(self, color=(1.0, 1.0, 1.0), on=0.0, off=0.0, fade_in=1.0, fade_out=1.0, cycles=1):
        i = 0
        step = 0.01
        on_steps = int(on/step)
        off_steps = int(off/step)
        fade_in_steps = int(fade_in/step)
        fade_out_steps = int(fade_out/step)
        while i < cycles:
            self.off()
            for s in range(off_steps):
                time.sleep(step)
            for s in range(fade_in_steps):
                self.on(color, s/(fade_in_steps-1))
                time.sleep(step)
            for s in range(on_steps):
                time.sleep(step)
            for s in range(fade_out_steps):
                self.on(color, (1-s/(fade_out_steps-1)))
                time.sleep(step)

if __name__ == '__main__':
    led = NavioLED()
    led.pulse(led.RED)
    led.pulse(led.BLUE)
    led.pulse(led.GREEN)
    led.pulse(led.PURPLE)
    led.pulse(led.YELLOW)
    led.pulse(led.CYAN)
