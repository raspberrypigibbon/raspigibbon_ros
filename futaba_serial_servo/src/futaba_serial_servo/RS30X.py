#!/usr/bin/env python
# coding:utf-8

"""
RS30X.py

Copyright (c) 2017 Shota Hirama <brast351-github@yahoo.co.jp>
Copyright (c) 2017 Daisuke Sato <tiryoh@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import serial
import struct


class RS304MD(object):
    def __init__(self, port = "/dev/ttyUSB0"):
        PORT = port
        BAUDRATE = 115200
        BYTESIZE = serial.EIGHTBITS
        PARITY = serial.PARITY_NONE
        STOPBIT = serial.STOPBITS_ONE
        TIMEOUT = 1
        self.ser = serial.Serial(PORT, BAUDRATE, BYTESIZE, PARITY, STOPBIT, TIMEOUT)

    def __del__(self):
        self.ser.close()

    def __bytecreateid(self, id):
        return [0xFA, 0xAF, id]

    def __checksum(self, checklist):
        sum = 0
        for i in range(2, len(checklist)):
            sum ^= checklist[i]
        checklist.append(sum)
        return checklist

    def __write(self, servolist):
        self.ser.write("".join(map(chr, servolist)))

    def __requestStatus(self, servo_id):
        a = self.__bytecreateid(servo_id)
        a.extend([0x09, 0x00, 0x00, 0x01])
        self.__write(self.__checksum(a))

    def __flash(self, servo_id):
        a = self.__bytecreateid(servo_id)
        a.extend([0x40, 0xFF, 0x00, 0x00])
        self.__write(self.__checksum(a))

    def setAngle(self, servo_id, set_angle):
        angle = max(-150.0, min(150.0, set_angle))
        angle = int(angle * 10)
        a = self.__bytecreateid(servo_id)
        a.extend([0x00, 0x1E, 0x02, 0x01, (angle & 0xFF), (angle & 0xFF00) >> 8])
        self.__write(self.__checksum(a))

    def setAngleInTime(self, servo_id, set_angle, set_goal_time):
        angle = max(-150.0, min(150.0, set_angle))
        angle = int(angle * 10)
        goal_time = int(set_goal_time * 100)
        a = self.__bytecreateid(servo_id)
        a.extend([0x00, 0x1E, 0x04, 0x01, angle & 0xFF, (angle & 0xFF00) >> 8, goal_time & 0xFF, (goal_time & 0xFF00) >> 8])
        self.__write(self.__checksum(a))

    def setTorque(self, servo_id, onoff):
        a = self.__bytecreateid(servo_id)
        a.extend([0x00, 0x24, 0x01, 0x01, int(onoff)])
        self.__write(self.__checksum(a))

    def setBreak(self, servo_id, onoff):
        if onoff == 1 : self.setTorque(servo_id, 2)
        else : self.setTorque(servo_id, onoff)

    def setServoId(self, servo_id, dest):
        a = self.__bytecreateid(servo_id)
        a.extend([0x00, 0x04, 0x01, 0x01, dest])
        self.__write(self.__checksum(a))
        self.__flash(servo_id)

    def setMaxTorque(self, servo_id, max_torque):
        a = self.__bytecreateid(servo_id)
        a.extend([0x00, 0x23, 0x01, 0x01, int(max_torque)])
        self.__write(self.__checksum(a))
        self.__flash(servo_id)

    def readAngle(self, servo_id):
        self.__requestStatus(servo_id)
        b = self.ser.read(26)[7:9]
        return struct.unpack("<h", b)[0] / 10.0

    def readTime(self, servo_id):
        self.__requestStatus(servo_id)
        b = self.ser.read(26)[9:11]
        return struct.unpack("<h", b)[0] * 10

    def readSpeed(self, servo_id):
        self.__requestStatus(servo_id)
        b = self.ser.read(26)[11:13]
        return struct.unpack("<h", b)[0]

    def readCurrent(self, servo_id):
        self.__requestStatus(servo_id)
        b = self.ser.read(26)[13:15]
        return struct.unpack("<h", b)[0]

    def readTemperature(self, servo_id):
        self.__requestStatus(servo_id)
        b = self.ser.read(26)[15:17]
        return struct.unpack("<h", b)[0]

    def readVoltage(self, servo_id):
        self.__requestStatus(servo_id)
        b = self.ser.read(26)[17:19]
        return struct.unpack("<h", b)[0] * 10

    def readTorqueStatus(self, servo_id):
        a = self.__bytecreateid(servo_id)
        a.extend([0x0F, 0x24, 0x02, 0x00])
        self.__write(self.__checksum(a))
        b = self.ser.read(9)[7:9]
        return struct.unpack("<h", b)[0]

    def reboot(self, servo_id):
        a = self.__bytecreateid(servo_id)
        a.extend([0x20, 0xFF, 0x00, 0x00])
        self.__write(self.__checksum(a))

