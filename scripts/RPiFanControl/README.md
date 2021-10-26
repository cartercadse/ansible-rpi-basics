# Control a PWM Fan on a Raspberry Pi

Tested on Raspberry Pi 3B+ and 4B but should work on other versions as well. 

# Installation

* Connect PWM capable Fan to GND, 5V and GPIO 12 (Pin 32)
* Copy or link RPiFanControl.service to /etc/systemd/system/RPiFanControl.service
  * `sudo ln -s $PWD/RPiFanControl.service /etc/systemd/system/RPiFanControl.service`
* Copy or link RPiFanControl.py to /usr/local/bin/RPiFanControl.py
  * `sudo ln -s $PWD/RPiFanControl.py /usr/local/bin/RPiFanControl.py` 
* Install python requirements
  * Run `sudo pip3 install -r requirements.txt`
* Enable system service
  * Run `sudo systemctl enable RPiFanControl`
* Add `dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4` to /boot/config.txt and 
* **Reboot your Pi**
