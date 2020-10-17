#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import telepot
import arduino
from datetime import datetime
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

command_list = [ 'Led On', 'Led Off', 'Fan On', 'Fan Off', 'Fan Sleep',
                'Alarm', 'Backlight', 'Get fan sleep', 'Get climate', 'Get sensor']

setter_list = ['MinTemp', 'MaxTemp', 'MinHum', 'MaxHum', 'Set sensor']

mainKeyboard = ReplyKeyboardMarkup(keyboard=[
                ['Info', 'Led On', 'Led Off',],
                ['Fan On', 'Fan Off'],
                ['Adjustments', 'Backlight'],
                ])

settingsKeyboard = ReplyKeyboardMarkup(keyboard=[
                ['MinTemp', 'MaxTemp'],
                ['MinHum', 'MaxHum'],
                ['Get climate', 'Get fan sleep', 'Get sensor', 'Set sensor', 'Main Menu']
                ])

climateKeyboard = ReplyKeyboardMarkup(keyboard=[
                ['30%', '40%', '50%', '60%', '70%', '80%'],
                ['20', '22', '23', '24', '25', '26', '27']
                ])

settings = False
climateAdjustment = False
last_setter = None

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global settings
    global climateAdjustment
    global last_setter

    if content_type == 'text':
        message = msg['text']
        user = msg['from']
        user = user['username']
        messageTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('\n' + "Command: {} "+'\n' + "From: {} " + 'Time: ' + '{}').format(message, user, messageTime)

        if message == 'Info':
            sensors = arduino.getInfo()
            bot.sendMessage(chat_id, "Temperature: {} Humidity: {}".format(sensors[0], sensors[1]), reply_markup=mainKeyboard)
#            print("Reply: Temp: {} Hum: {}".format(sensors[0], sensors[1]))

        elif message in command_list:
            reply = arduino.sendCommand(message)
            bot.sendMessage(chat_id, reply, reply_markup=mainKeyboard)
#           print("Reply: {}".format(reply) )

        elif message == 'Adjustments':
            bot.sendMessage(chat_id, 'Here you can tune some settings.', reply_markup=settingsKeyboard)
            settings = True

        elif settings:
            if message == 'Main Menu':
                bot.sendMessage(chat_id, 'Available commands.', reply_markup=mainKeyboard)
            else:
                if message in setter_list:
                    settings = False
                    climateAdjustment = True
                    last_setter = message
                    bot.sendMessage(chat_id, 'Set the value for {}'.format(last_setter), reply_markup=climateKeyboard)
        elif climateAdjustment:
            reply = arduino.sendSetter(last_setter, message[0:2])
            # bot.sendMessage(chat_id, message[0:2], reply_markup=mainKeyboard)
            bot.sendMessage(chat_id, reply, reply_markup=mainKeyboard)
            climateAdjustment = False

        else:
            bot.sendMessage(chat_id, 'Unknown command. Please, use keyboard.', reply_markup=mainKeyboard)


TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
MessageLoop(bot, on_chat_message).run_as_thread()
print ('Listening ...' + '\n')

while 1:
    time.sleep(20)
