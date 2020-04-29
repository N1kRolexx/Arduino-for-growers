# Arduino for growers 

This project allows for automation of growing processes and on-the-fly control and adjustment of your growing environment.

Arduino is the heart of this project and is responsible for controlling relays and sensors. Raspbery Pi with a Telegram bot onboard is the brain, which controls Arduino through a serial connection.

I decided to write this project to fulfill some of my needs as a grower a while ago. Then, after some amount of features had accumulated, I though this project could be useful for someone, who is growing indoors and would like to add some automation to their growing process :) 

Also, similar controllers, whilst not having same functionality, are pretty expensive on market, whereas this project would cost you nearly 60$ and even cheaper if order everything from China.

---
## Features
- Telegram bot with nice menu, which allows full control over your growing environment.
- Measuring temperature/humidity and showing on LCD display inside grow space or sending to you via Telegram.
- Automatic climate control allows to set temperature and humidity levels, which Arduino will try to keep to during different stages of growing.
- Automatic 18/6 or manual light schedule for your plants.
- All adjustments are done through Telegram bot menu.
---
## What you will need
### Hardware
- Raspberry Pi (Pi Zero W would be enough)
- Arduino microcontroller (I recommend Arduino Uno/Nano)
- DHT22 Sensor
- 16x2 or 20x4 LCD display
- 4-channel Solid State Relay (solid state relays don't produce any noise)
- ds3231 Real Time Clock

### Software
- Python 2.7 (Comes preinstalled on Raspbian)
- Telepot - telegram bot library for python (https://github.com/nickoala/telepot)
- PySerial - serial port access library for python (https://github.com/pyserial/pyserial)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies 

```bash
pip install pyserial
pip install telepot
```
---
## Usage
To start bot in the background and suppress output:
```bash
sudo nohup python bot.py &
```
----
## Upcoming features & Plans
- Soil moisture measurements & Automatic watering.
- CO2 measurements inside grow space.
- Motion Sensor to detect movement near growbox.
- RFID card access to your growing area.
- Rewrite python bot using another library, because telepot is deprecated already.
- Port everything to NodeMCU development board to get rid of Raspberry Pi and serial connection.

## Contributing
Pull requests are welcome. In general, any changes/propositions/requests are welcome. I would be happy if someone finds a use for my project or even improves it somehow.

## Disclaimer
I am not a professional programmer, therefore this code consists of 50% YouTube lessons, 25% stack overflow and 25% documentation. I am not responsible for mental illnesses you could receive after reading it :P

## License
[MIT](https://choosealicense.com/licenses/mit/)
