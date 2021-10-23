# Installation

Connect PWM capable Fan to GND, 5V and GPIO 12 (Pin 32)

Copy or link RPiFanControl.service to /etc/systemd/system/RPiFanControl.service, make sure it's executable  
Copy or link RPiFanControl.py to /usr/local/bin/RPiFanControl.py  

First run  `sudo systemctl enable RPiFanControl`

Then `sudo systemctl start RPiFanControl`  
