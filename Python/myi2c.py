import smbus
import time
from signal import pause
from gpiozero import LED

i2cbus = smbus.SMBus(1)
address = 0x40

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

def set_all_pwm(bus, on, off):
    """Sets all PWM channels"""
    bus.write_byte_data(address, __ALL_LED_ON_L, on & 0xFF)
    bus.write_byte_data(address, __ALL_LED_ON_H, on >> 8)
    bus.write_byte_data(address, __ALL_LED_OFF_L, off & 0xFF)
    bus.write_byte_data(address, __ALL_LED_OFF_H, off >> 8)

def set_pwm(bus, channel, duty_cycle=0.5, delay=0):
    if (delay + duty_cycle <= 1):
        on = int(delay*4095)
        off = int(duty_cycle*4095) + on
        bus.write_byte_data(address, __LED0_ON_L + 4 * channel, on & 0xFF)
        bus.write_byte_data(address, __LED0_ON_H + 4 * channel, on >> 8)
        bus.write_byte_data(address, __LED0_OFF_L + 4 * channel, off & 0xFF)
        bus.write_byte_data(address, __LED0_OFF_H + 4 * channel, off >> 8)

def set_led(bus, channel, saturation=1):
    set_pwm(bus, channel, 1-saturation)

# Init
pin = LED(27)
pin.off()

set_all_pwm(i2cbus, 0, 0)
i2cbus.write_byte_data(address, __MODE2, __OUTDRV)
i2cbus.write_byte_data(address, __MODE1, __ALLCALL)
time.sleep(0.005)  # wait for oscillator

mode1 = i2cbus.read_byte_data(address, __MODE1)
mode1 = mode1 & ~__SLEEP  # wake up (reset sleep)
i2cbus.write_byte_data(address, __MODE1, mode1)
time.sleep(0.005)  # wait for oscillator

set_led(i2cbus, 2, 0)
set_led(i2cbus, 1, 0)
set_led(i2cbus, 0, 0)
print("dark")
time.sleep(2)
set_led(i2cbus, 2, 1)
print("red")
time.sleep(2)
set_led(i2cbus, 2, 0)
set_led(i2cbus, 0, 1)
print("blue")
time.sleep(2)
set_led(i2cbus, 0, 0)
set_led(i2cbus, 1, 1)
print("green")
time.sleep(2)
pause()
