#!/usr/bin/env python3

"""
Controls a PWM capable fan connected to a PWM pin on the Raspberry Pi

Written by Qetesh

To enable hardware pwm, add to /boot/config.txt: dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4
This will enable pwm channel 0 on GPIO 12 (PIN 32) and channel 1 on GPIO 13 (PIN 33)
Don't forget to reboot for this to have an effect
"""


from rpi_hardware_pwm import HardwarePWM
from time import sleep
import signal
import random

CHANNEL = 0    # PWM Channel - 0 or 1
MINTEMP = 40   # Minimum temperature in °C - fan is off below this value
MAXTEMP = 60   # Maximum temperature in °C - fan is at 100%
MINDC = 20     # Minimum Duty Cycle for the fan
MAXDC = 100    # Maximum Duty Cycle for the fan
SLEEPTIME = 5  # time in seconds between updates


class PWMFan:
    def __init__(self,
                 PWMChannel: int = 0,
                 mintemp: int = 30,
                 maxtemp: int = 60,
                 mindc: int = 20,
                 maxdc: int = 100
                 ) -> None:
        """
        :param PWMChannel: 0 or 1
        :param mintemp: Temperature less than this and the fan is off
        :param maxtemp: Temperature more than this and the fan runs full speed
        """
        self.mintemp = mintemp
        self.maxtemp = maxtemp
        self.mindc = mindc
        self.maxdc = maxdc
        self.pwm = HardwarePWM(PWMChannel, hz=25000)
        self.pwm.start(0)
        self.running = True
        print("Starting the fan controller...")
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGHUP, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, signum, frame) -> None:
        print(F"Signal {signum} cought in frame {frame}")
        print("Stopping the fan controller...")
        self.running = False
        self.pwm.stop()

    def updateFan(self) -> None:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as t:
                temperature = int(t.readline().strip()) / 1000
        except FileNotFoundError:
            # generate random values for testing on non-Pi
            temperature = random.randint(20, 70)
        if temperature < self.mintemp:
            # fan is off when temp below mintemp
            dc = 0
        elif temperature > self.maxtemp:
            # fan is fully on when temp above maxtemp
            dc = 100
        else:
            # calculate duty cycle when temp is between min and max
            dc = int((temperature - self.mintemp) * (self.maxdc - self.mindc) /
                     (self.maxtemp - self.mintemp) + self.mindc)
        # set duty cycle
        self.pwm.change_duty_cycle(dc)
        # print out temperature and dc
        print(f"Temperature: {temperature:4.2f}°C - DutyCycle: {dc}%")


def main():
    fan = PWMFan(PWMChannel=CHANNEL, mintemp=MINTEMP, maxtemp=MAXTEMP, mindc=MINDC, maxdc=MAXDC)
    while fan.running:
        fan.updateFan()
        # sleep some time
        sleep(SLEEPTIME)


if __name__ == "__main__":
    main()
