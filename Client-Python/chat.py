from socket import *
from socket import ssl as sslc
from threading import Thread
import settings


def recv(s):
    data = s.read(1024)
    try:
        return data[:1], data[1:]  # return data
    except:
        return None


def main():
    print "Run with -t for terminal ver"
    

def bash():
    if settings.host == "": host = raw_input("Server: ")
    else: host = settings.host
    if settings.port == "": port = raw_input("Port: ")
    else: port = settings.port
    global running
    running = True
    uws = socket(AF_INET, SOCK_STREAM)
    uws.connect((host, port))
    s = ssl(uws)
    global username
    if settings.username == "": username = raw_input("Username: ")
    else: username = settings.username
    s.write("\x00"+username)
    pType, data = recv(s)
    while data != "incorect"and pType == "\x01":
        passwd = raw_input("Password: ")
        print "loading please wait"
        s.write("\x01"+passwd)
        pType, data = recv(s)

    if data == "make":
        make = "  "
        while make not in ["n","N","y","Y",""]:
            make = raw_input("User does not exist make user.(y/[n]): ")
        if make != "":
            s.write("\x03"+make.replace("N","n").replace("Y","y"))
        else:
            s.write("\x03"+"n")
        pType, data = recv(s)
        if make.replace("Y","y") == "y" and pType == "\01":
            passwd = raw_input("Password: ")
            print "loading please wimport sslait"
            s.write("\x01"+passwd)

        else:
            running = False

    if running:
        print "\n"+data
        print "Connected"
        rthread = Thread(target = recive, args = (s, ))
        rthread.start()
    while running:
        message = raw_input("")
        if message == "quit":
            s.write("quit")
            uws.close()
            running = False
            break;
        if message != "":
            s.write("\x05"+username+": "+message)

def recive(s):
    global running
    while running:
        try:
            pType, data = recv(s)
            if not data: break
        except Exception, e:
            running = False"""
websocket - WebSocket client library for Python

Copyright (C) 2010 Hiroki Ohtani(liris)

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA 02110-1335  USA

"""

import six

__all__ = ["NoLock", "validate_utf8", "extract_err_message"]

class NoLock(object):
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

try:
    # If wsaccel is available we use compiled routines to validate UTF-8
    # strings.
    from wsaccel.utf8validator import Utf8Validator

    def _validate_utf8(utfbytes):
        return Utf8Validator().validate(utfbytes)[0]

except ImportError:
    # UTF-8 validator
    # python implementation of http://bjoern.hoehrmann.de/utf-8/decoder/dfa/

    _UTF8_ACCEPT = 0
    _UTF8_REJECT = 12

    _UTF8D = [
        # The first part of the table maps bytes to character classes that
        # to reduce the size of the transition table and create bitmasks.
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,  9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
        7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,  7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
        8,8,2,2,2,2,2,2,2,2,2,2,2,2,2,2,  2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
        10,3,3,3,3,3,3,3,3,3,3,3,3,4,3,3, 11,6,6,6,5,8,8,8,8,8,8,8,8,8,8,8,

        # The second part is a transition table that maps a combination
        # of a state of the automaton and a character class to a state.
        0,12,24,36,60,96,84,12,12,12,48,72, 12,12,12,12,12,12,12,12,12,12,12,12,
        12, 0,12,12,12,12,12, 0,12, 0,12,12, 12,24,12,12,12,12,12,24,12,24,12,12,
        12,12,12,12,12,12,12,24,12,12,12,12, 12,24,12,12,12,12,12,12,12,24,12,12,
        12,12,12,12,12,12,12,36,12,36,12,12, 12,36,12,12,12,12,12,36,12,36,12,12,
        12,36,12,12,12,12,12,12,12,12,12,12, ]

    def _decode(state, codep, ch):
        tp = _UTF8D[ch]

        codep = (ch & 0x3f ) | (codep << 6) if (state != _UTF8_ACCEPT)  else (0xff >> tp) & (ch)
        state = _UTF8D[256 + state + tp]

        return state, codep;

    def _validate_utf8(utfbytes):
        state = _UTF8_ACCEPT
        codep = 0
        for i in utfbytes:
            if six.PY2:
                i = ord(i)
            state, codep = _decode(state, codep, i)
            if state == _UTF8_REJECT:
                return False

        return True

def validate_utf8(utfbytes):
    """
    validate utf8 byte string.
    utfbytes: utf byte string to check.
    return value: if valid utf8 string, return true. Otherwise, return false.
    """
    return _validate_utf8(utfbytes)

def extract_err_message(exception):
    if exception.args:
        return exception.args[0]
    else:
        return None

        if pType == "\x04" or pType == "\x05":
            print data
