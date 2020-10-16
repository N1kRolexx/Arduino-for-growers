#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import telepot
import arduinotest as arduino
from datetime import datetime
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


welcome_msg = "Hi there!" + u'\U0001f44b' + " I am GrowBot.\nI will manage your grow environment" + u'\U0001f340' + '\n' + "\nI have handy keyboards" + u'\U0001f3b9' + "so "
welcome_msg += "you can easily control all processes in your tent/growbox/greenhouse." + '\n' + '\n' + u'\u2753' + "Type /help to see what I can do. Have fun " + u'\U0001f919'

help_msg =  "\n" + u'\U0001f321' + "Get info - you are going to use this a lot :) It will simply show you current data from sensors." + "\n"
help_msg += "\n" + u'\U0001f326' + "Climate control section - allows to tune minimal and maximal temperature and humidity in your "
help_msg += "grow environment. Arduino will try to keep these levels by switching on/off the exhaust fan and humidifier."
help_msg += "\n" + u'\u2614' + "Current Settings - will show you what are the current climate levels. \n" + u'\U0001f321' + "By clicking \"min temp/hum\""+ "and \"max temp/hum\" buttons "
help_msg += "you can change these levels. You can write numbers on your own, but I recommend using keyboard for optimal values."
help_msg += "\n" + u'\u23f3' + "Set sensor - tell arduino how often (in seconds) it should retrieve data from sensors." + "\n"
help_msg += "\n" + u'\u26fa' + "Facility operation - in this section you can directly turn on/off the fan, LED and humidifier, if you have one. Also, you can put fan to sleep mode, "
help_msg += " and it will not work for a certain period of time. For example, if Fan's noise interferes your sleep."
help_msg += "\n" + u'\U0001f6a8' + "Alarm button will turn off everything in your tent."
help_msg += "\n" + u'\U0001f526' + "Switch LCD - toggle Arduino's LCD display backlight." + "\n"
help_msg += "\n" + u'\u2755' + "Type /tip to show an advice about how everything works."

tip_msg = "Everything is built aroung sensor update cycle. Default time is 5 seconds. After new data is received, arduino checks if the fan "
tip_msg += "should work, whether it is time for the Led to shine and whether the (de)humidifier should induce a mist." + "\n"
tip_msg += "If you want to turn off the LED for some time (for example, for it not to shine in your eyes during some operations in tent) you can set a longer sensor update time, "
tip_msg += "turn Led off in \"Facility\" section and do your thing. The same with the Fan, humidifier and LCD display." + "\n"
tip_msg += "\nYou can also write commands directly to you bot at any time, without built-in keyboards. \nCurrently avalable commands are from \"Facility\" "
tip_msg += "section only: led on, led off, fan on, fan off, fan sleep, alarm, backlight, get fan sleep, get climate, get sensor (not case sensitive)."


MainMenuKeyboard = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                [u'\U0001f321' + ' Get info'],
                [u'\U0001f326' + ' Climate control', u'\u26fa' + ' Facility operation'] ])

climateKeyb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=u'\u2614' +' Current settings', callback_data='get climate')],
                [InlineKeyboardButton(text=u'\u2744' + ' Min temp', callback_data='mintemp'), InlineKeyboardButton(text=u'\u2600' + ' Max temp', callback_data='maxtemp')],
                [InlineKeyboardButton(text=u'\U0001f4a7' + "Min hum", callback_data='minhum'), InlineKeyboardButton(text=u'\U0001f4a6' + ' Max hum', callback_data='maxhum')],
                [InlineKeyboardButton(text=u'\u23f3' + ' Set sensor', callback_data='set sensor')],
                [InlineKeyboardButton(text='Main menu', callback_data='main menu')]
               ])
facilityKeyb = InlineKeyboardMarkup(inline_keyboard=[
                 [InlineKeyboardButton(text='Led on ' + u'\U0001f315', callback_data='led on'), InlineKeyboardButton(text='Led off ' + u'\U0001f318', callback_data='led off')],
                 [InlineKeyboardButton(text='Fan On ' + u'\U0001f32c', callback_data='fan on'), InlineKeyboardButton(text='Fan off ' + u'\u2716', callback_data='fan off')],
                 [InlineKeyboardButton(text='Fan sleep ' + u'\U0001f4a4', callback_data='fan sleep'), InlineKeyboardButton(text='Alarm!' + u'\U0001f6a8', callback_data='alarm')],
                 [InlineKeyboardButton(text='Switch LCD backlight ' + u'\U0001f526', callback_data='backlight')],
                 [InlineKeyboardButton(text='Main menu', callback_data='main menu')]
                ])

tempKeyb = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                ['17', '18', '19', '20', '21', '22'],
                ['23', '24', '25', '26', '27', '28']
                ])
humidityKeyb = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                ['10%', '20%', '30%', '40%', '50%'],
                ['60%', '70%', '80%', '90%','100%']
                ])
sensorKeyb = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                ['3', '5', '10', '15', '30'],
                ['60', '300', '600', '1800']
                ])

commandsList = [ 'led on', 'led off', 'fan on', 'fan off', 'fan sleep', 'alarm',    # commands, which are understood by arduino, so can be sent directly to it
                 'backlight', 'get fan sleep', 'get climate', 'get sensor',]
setterList = ['mintemp', 'maxtemp', 'minhum', 'maxhum', 'set sensor']               # setters


deleteKeyb = ReplyKeyboardRemove()
message_with_keyb = None
climate_settings = False
last_setter = None


def on_chat_message(msg):
    global climate_settings    # a flag to enter 2nd keyboard level
    global last_setter          # var to remember last setter option bofore receiving it's value and sending them to arduino
    global message_with_keyb
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        message = msg['text']               # store user message for further parsing
        user = msg['from']['username']      # who send the command

        messageTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')              # store the time of received message
        logger = '\n' + "Command: {} " + '\n' + 'From: {} ' + 'Time: ' + '{}'   # prepare information for printing
        print(logger).format(message.encode('utf-8'), user, messageTime)                        # print all commands received by bot

        if message.startswith('/start'):
            bot.sendMessage(chat_id, welcome_msg, reply_markup=MainMenuKeyboard)
        elif message.startswith('/help'):
            bot.sendMessage(chat_id, help_msg, reply_markup=MainMenuKeyboard)
        elif message.startswith('/tip'):
            bot.sendMessage(chat_id, tip_msg, reply_markup=MainMenuKeyboard)

        elif message.lower() in commandsList:           # you can also write commands directly to bot, without built-in keyboard (not case sensitive)
            climate_settings = False                    # prevent the user from staying with climateKeyboard, if issued a direct command to bot.
            reply = arduino.sendCommand(message)        # sned command to arduino
            bot.sendMessage(chat_id, reply, reply_markup=MainMenuKeyboard)  # return answer from arduino

        elif message == u'\U0001f321' + ' Get info':             # get temperature and humidity from arduino
            sensors = arduino.getInfo()
            bot.sendMessage(chat_id, "Temperature: {} Humidity: {}".format(sensors[0], sensors[1]) )
        elif message == u'\u26fa' + ' Facility operation':   # show facility control menu
            message_with_keyb = bot.sendMessage(chat_id,'Control facility with one click '+ u'\u2699', reply_markup=facilityKeyb)
        elif message == u'\U0001f326' + ' Climate control':      # enter climate control manu
            message_with_keyb = bot.sendMessage(chat_id, 'Here you can control the climate' + u'\U0001f326', reply_markup=climateKeyb)

        elif climate_settings:                  # if a user has choosen a 'setter' in Climate control menu - parse next message as a value for that setter
            message = message.split('%')        # cut degree sign
            if message[0].isnumeric():          # check if input is appropriate
                reply = arduino.sendSetter(last_setter, message[0])     # send setter and numeric value to arduino
                bot.answerCallbackQuery(query_id, reply)                # show the user a result, received from arduino
                climate_settings = False        # finish climate adjustment
        else:
            bot.sendMessage(chat_id, 'Hmm.. I dont know this command. Try to use keyboard ;)', reply_markup=MainMenuKeyboard)


def on_callback_query(msg):
    global climate_settings         # a flag to enter 2nd keyboard level
    global last_setter              # var to remember last setter option bofore receiving it's value and sending them to arduino
    global query_id                 # remember last inline keyboard sent, to hide it later
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('\n' + "Query: {} "+'\n' + "From: {} " + 'Time: ' + '{}').format(query_data, from_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))        # print activity

    if query_data in commandsList:              # send command (if appropriate) directly to arduino
        reply = arduino.sendCommand(query_data)
        bot.answerCallbackQuery(query_id, reply)
        climate_settings = False

    if query_data == 'main menu':        #hide last inline keyb and show main manu
        global message_with_keyb
        if message_with_keyb:
            msg_idf = telepot.message_identifier(message_with_keyb)
            bot.editMessageText(msg_idf, 'Changed your mind?')
        else:
            bot.answerCallbackQuery(query_id, text='No previous message to edit')
        bot.sendMessage(from_id, 'Here is the main menu :)', reply_markup=MainMenuKeyboard)

    if query_data == 'mintemp':         #define Temperature levels
        climate_settings = True
        last_setter = query_data
        bot.sendMessage(from_id, 'Choose minimal temperature level', reply_markup=tempKeyb)
    if query_data == 'maxtemp':
        climate_settings = True
        last_setter = query_data
        bot.sendMessage(from_id, 'Choose maximal temperature level', reply_markup=tempKeyb)
    if query_data == 'minhum':          #define humidity levels
        climate_settings = True
        last_setter = query_data
        bot.sendMessage(from_id, 'Choose minimal humidity level', reply_markup=humidityKeyb)
    if query_data == 'maxhum':
        climate_settings = True
        last_setter = query_data
        bot.sendMessage(from_id, 'Choose maximal humidity level', reply_markup=humidityKeyb)
    if query_data == 'set sensor':      #tell arduino how often to update sensor
        climate_settings = True
        last_setter = query_data
        bot.sendMessage(from_id, 'How often should I update sensors?', reply_markup=sensorKeyb)



bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

print ('Listening ...' + '\n')          #print that the bot has started polling

while 1:
    time.sleep(20)
