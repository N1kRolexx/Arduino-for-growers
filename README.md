# Arduino for growers 

Automate indoor growing with the help of Arduino, Raspberry Pi and Python Telegram bot. This project allows for automation of growing processes and on-the-fly control and adjustment of your growing environment.

I decided to write this project to fulfill some of my needs as a grower a while ago. Then, after some amount of features have accumulated, I though this could be useful for someone :) 


Arduino is the heart of this project and is responsible for controlling relays and sensors. Raspbery Pi with a Telegram bot onboard is the brain, which controls Arduino through a serial connection.

## Features
- Telegram bot with nice menu, which allows full control over your growing environment.
- Measuring temperature/humidity and showing on LCD display inside grow space or sending to you via Telegram.
- Automatic climate control allows to set temperature/humidity levels during different stages of growing.
- Automatic 18/6 or manual light schedule for your plants.

## Setup

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyserial

```bash
pip install pyserial
```

## Usage

## Upcoming features
- Soil moisture measurements & Automatic watering.
- CO2 measurements inside grow space.
- Motion Sensor to detect movement near growbox.
- RFID card access to your growing area.

## Contributing
Pull requests are welcome. In general, any changes/propositions/requests are welcome. I would be happy if someone finds a use for my project or even improves it.

## Disclaimer
I am not a professional programmer, therefore this code consists of 50% YouTube lessons, 25% stack overflow and 25% documentation. I am not responsible for mental illnesses you could receive after reading it :P

## License
[MIT](https://choosealicense.com/licenses/mit/)
