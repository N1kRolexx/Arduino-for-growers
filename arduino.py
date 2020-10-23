#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial


ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyAMA0'    # usual port on Raspbian, use "python -m serial.tools.list_ports" to determine the port
ser.timeout = 1
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
