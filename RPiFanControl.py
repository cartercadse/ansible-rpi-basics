#!/usr/bin/env python3
"""
Controls a PWM capable fan connected to a PWM pin on the Raspberry Pi

Copyright © 2021 Qetesh
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the LICENSE file for more details.

To enable hardware pwm, add to /boot/config.txt: dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4
This will enable pwm channel 0 on GPIO 12 (PIN 32) and channel 1 on GPIO 13 (PIN 33)
Don't forget to reboot for this to have an effect
"""

from rpi_hardware_pwm import HardwarePWM
from time import sleep
import signal
import pathlib
import os

CHANNEL = 0         # PWM Channel - 0 or 1
MINTEMP = 40        # Minimum temperature in °C - fan is off below this value
MAXTEMP = 60        # Maximum temperature in °C - fan is at 100%
MINDC = 20          # Minimum Duty Cycle for the fan
MAXDC = 100         # Maximum Duty Cycle for the fan
SLEEPTIME = 5       # time in seconds between updates
WRITEFILES = True   # write current temperature and dutycycle into files in run directory for external use


class PWMFan:
    def __init__(self,
                 PWMChannel: int = 0,
                 mintemp: int = 30,
                 maxtemp: int = 60,
                 mindc: int = 20,
                 maxdc: int = 100,
                 writeFiles: bool = True
                 ) -> None:
        """
        :param PWMChannel: 0 or 1
        :param mintemp: Temperature less than this and the fan is off
        :param maxtemp: Temperature more than this and the fan runs full speed
        :param mindc: Minimum duty cycle for the fan
        :param maxdc: Maximum duty cycle for the fan
        :param writeFiles: write current temperature and dutycycle into files in run directory for external use
        """
        self.mintemp = mintemp
        self.maxtemp = maxtemp
        self.mindc = mindc
        self.maxdc = maxdc
        self.pwm = HardwarePWM(PWMChannel, hz=25000)
        self.pwm.start(0)
        self.running = True
        self.cwd = str(pathlib.Path.cwd())
        self.tempfile = self.cwd + "/temperature"
        self.dcfile = self.cwd + "/dutycycle"
        self.writeFiles = writeFiles
        self.lasttemp = 0
        print("CWD:", self.cwd)
        if self.writeFiles:
            print("Temperature File:", self.tempfile)
            print("Duty Cycle File:", self.dcfile)
        print("Starting the fan controller...")
        signal.signal(signal.SIGINT, self._sig)
        signal.signal(signal.SIGHUP, self._sig)
        signal.signal(signal.SIGTERM, self._sig)

    def _sig(self, signum, frame) -> None:
        print(F"{signal.Signals(signum).name} ({signum}) cought in frame {frame}")
        self.stop()

    def stop(self) -> None:
        print("Stopping the fan controller...")
        self.running = False
        self.pwm.stop()
        if os.path.exists(self.tempfile):
            os.remove(self.tempfile)
        if os.path.exists(self.dcfile):
            os.remove(self.dcfile)

    def updateFan(self) -> None:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as t:
                temperature = int(t.readline().strip()) / 1000
        except FileNotFoundError:
            print("/sys/class/thermal/thermal_zone0/temp not found, using max value")
            temperature = self.maxtemp
        if temperature != self.lasttemp:
            self.lasttemp = temperature
            if temperature < self.mintemp:
                # fan is off when temp below mintemp
                dc = 0
            elif temperature >= self.maxtemp:
                # fan is fully on when temp above maxtemp
                dc = 100
            else:
                # calculate duty cycle when temp is between min and max
                dc = int((temperature - self.mintemp) * (self.maxdc - self.mindc) /
                         (self.maxtemp - self.mintemp) + self.mindc)
            # set duty cycle
            self.pwm.change_duty_cycle(dc)
            # print out temperature and dc
            print(f"Temperature: {temperature:4.1f}°C - DutyCycle: {dc}%")
            if self.writeFiles:
                # write temperature and dutycycle values to files in run directory
                try:
                    with open(self.tempfile, "w") as tempfile:
                        tempfile.write(str(temperature))
                except FileNotFoundError:
                    print("Can't write temperature file")
                try:
                    with open(self.dcfile, "w") as dcfile:
                        dcfile.write(str(dc))
                except FileNotFoundError:
                    print("Can't write dc file")


def main():
    fan = PWMFan(PWMChannel=CHANNEL, mintemp=MINTEMP, maxtemp=MAXTEMP, mindc=MINDC, maxdc=MAXDC, writeFiles=WRITEFILES)
    while fan.running:
        fan.updateFan()
        # sleep some time
        sleep(SLEEPTIME)


if __name__ == "__main__":
    main()
