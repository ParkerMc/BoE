import ssl
from struct import pack, unpack
from threading import Thread
from time import sleep

import websocket
from PyQt4.QtCore import pyqtSignal, QObject


class Socket(QObject):
    newMsg = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.server = ""
        self.port = 8000
        self.messages = []
        self.ws = None
        self.thread = None
        for i in range(0, 7):
            self.messages.append([])

    def connect(self, server, port):
        try:
            websocket.enableTrace(True)
            self.ws = websocket.WebSocketApp("wss://" + server + ":" + port, on_message=self.on_message,
                                             on_error=self.on_error, on_close=self.on_close)
            self.thread = Thread(target=self.ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}},
                                 name="socket")
            self.thread.daemon = True
            self.thread.start()
        except:
            self.ws = None

    def disconnect(self):
        if self.ws is not None:
            self.ws.send(pack(">i", 5) + "quit")
            sleep(.5)
            self.ws.close()
            self.ws = None

    def send(self, pid, msg):
        self.ws.send(str(pack(">i", pid)) + msg)

    def on_message(self, ws, message):
        print message
        pid = unpack(">i", message[:4])[0]
        print pid
        message = message[4:]
        print message
        self.messages[int(pid)].append(message)
        self.newMsg.emit()

    def waitTillMessage(self, stop=None, *pid):
        ids, messages = self.getMessages(*pid)
        while len(messages) == 0:
            ids, messages = self.getMessages(*pid)
            if stop is not None:
                if not stop.wait(1):
                    return None, None
        return ids, messages

    def getMessages(self, *pid):
        out = []
        ids = []
        for i in pid:
            i = int(i)
            for j in self.messages[i]:
                out.append(j)
                ids.append(i)
                self.messages[i].remove(j)
        return ids, out

    @staticmethod
    def on_error(ws, error):
        print error

    @staticmethod
    def on_close(ws):
        print "### closed ###"
