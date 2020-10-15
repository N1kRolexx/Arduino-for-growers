#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import serial


ser = serial.Serial()
ser.baudrate = 115200           # should match arduino's sketch baudrate
ser.port = '/dev/ttyAMA0'       # usual arduino port on Raspbian
ser.timeout = 1                 # important for not to freeze the program, if some messages did not arrive
ser.open()

def getInfo():
    ser.flushInput()
    ser.flushOutput()
    ser.write("info".encode() + "\n")
    sensors = ser.readline().split(";")
    return sensors

def sendCommand(command):
    ser.flushInput()
    ser.flushOutput()
    ser.write(command.encode() + "\n")
    reply = ser.readline()
    return reply

def sendSetter(setter, setterVal):
    ser.flushInput()
    ser.flushOutput()
    setter = "{0}:{1}".format(setter, setterVal)
    ser.write(setter.encode() + "\n")
    reply = ser.readline()
    return reply

# For testing purpose, when you have no arduino connected
# def getInfo():
#     sensors = "26;70".split(";")
#     return sensors
#
# def sendCommand(command):
#     reply = "received command: {}".format(command)
#     return reply
#
# def sendSetter(setter, setterVal):
#     reply = "setter: {} value: {}".format(setter, setterVal)
#     return reply
#
