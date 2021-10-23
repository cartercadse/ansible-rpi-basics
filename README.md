# Installation

Connect PWM capable Fan to GND, 5V and GPIO 12 (Pin 32)

Copy or link RPiFanControl.service to /etc/systemd/system/RPiFanControl.service, make sure it's executable  
Copy or link RPiFanControl.py to /usr/local/bin/RPiFanControl.py  

Add `dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4` to /boot/config.txt **and reboot your Pi**

Run `sudo systemctl enable RPiFanControl`

Run `sudo systemctl start RPiFanControl`  
