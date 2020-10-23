# Arduino for growers

This project allows for automation of growing processes and on-the-fly control and adjustment of your growing environment.

Arduino is the heart of this project and is responsible for controlling relays and sensors. Raspbery Pi with a Telegram bot onboard is the brain, which controls Arduino through a serial connection.

I decided to write this project to fulfill some of my needs as a grower a while ago. Then, after some amount of features had accumulated, I though this project could be useful for someone, who is growing indoors and would like to add some automation to their growing process :)

Also, similar controllers, whilst not having same functionality, are pretty expensive on market, whereas this project would cost you nearly 60$ and even cheaper if ordered from China.

## Key features
- Telegram bot with nice keyboards, which allows full control over your growing environment.
- Measuring temperature/humidity and showing on LCD display inside grow space or sending to you via Telegram.
- Automatic climate control. You can change temperature and humidity levels and arduino will try to keep them.
- Automatic 18/6 light schedule.
- All adjustments are done through Telegram bot menu and handy keyboards.
------------
## What you will need
### Hardware
- Raspberry Pi (Pi Zero W would be enough)
- Arduino (I recommend Uno/Nano)
- DHT22 Sensor
- 16x2 or 20x4 LCD display with I2C
- 4-channel Solid State Relay (solid state relays don't produce any noise)
- ds3231 Real Time Clock
- 400 pin prototype board
- Jumper Wires
- 10kOhm resistor and 10μf capacitor
- Bi-Directional Logic Level Converter 3.3v - 5v (Used for serial connection. Alternatively, you can connect arduino via USB, it is easier).

### Software
- Python 3.8
- Telepot - telegram bot library for python (https://github.com/nickoala/telepot)
- PySerial - serial port access library for python (https://github.com/pyserial/pyserial)

Use [pip](https://pip.pypa.io/en/stable/) to install dependencies.
```bash
pip3 install pyserial
pip3 install telepot
```
## How to set everything up
1. Connect all parts as shown on scheme.
Remember to put 10kOhm resistor between VCC and DATA pins of DHT22 sensor. Also, put 10μf capacitor between RST and GND pins to avoid reset when serial port opens. I recommend using external breabdoard PSU to power everything.
![](https://raw.githubusercontent.com/N1kRolexx/Arduino-for-growers/master/arduino-for-growers3_bb.png?token=AD6KLWXUI7Y5W22QEOLE42K7SL44Q)
2.  Open "arduino.py" and edit serial port address. Use python to determine correct address.
```python
python -m serial.tools.list_ports
```

3.  Then write '/start' to your Growbot!

## Usage
To start bot in the background and suppress output:
```bash
nohup python growbot-v2.py your_bot_token &
```
------------
## Upcoming features & Plans
- Soil moisture measurements & Automatic watering.
- Smiles in bot's menu and keyboards. ✓
- CO2 measurements inside grow space.
- Motion Sensor to detect movement near grow area.
- RFID card access to your growing area.
- Rewrite python bot using another library, because telepot is deprecated already.
- Port everything to NodeMCU development board to get rid of Raspberry Pi and serial connection.

## Contributing
Any changes/propositions/requests are welcome. I would be happy if someone finds a use for my project or even improves it somehow.

## Disclaimer
I am not a professional programmer, therefore this code consists of 50% YouTube lessons, 25% stack overflow and 25% documentation. I am not responsible for mental illnesses you could receive after reading it :P

## License
[MIT](https://choosealicense.com/licenses/mit/)
