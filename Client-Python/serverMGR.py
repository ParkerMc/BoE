import ssl
from struct import pack, unpack
from threading import Thread

from PyQt4.QtCore import pyqtSignal

import websocket


class Socket:
	def __init__(self):
		self.server = ""
		self.port = 8000
		self.messages = []
		for i in range(0, 7):
			self.messages.append([])
		self.newMsg = pyqtSignal()

	def connect(self, server, port):
		websocket.enableTrace(True)
		self.ws = websocket.WebSocketApp("wss://"+server+":"+port, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
		self.thread = Thread(target=self.ws.run_forever, kwargs={"sslopt":{"cert_reqs": ssl.CERT_NONE}}, name="socket")
		self.thread.start()

	def disconnect(self):
		self.ws.send(pack(">i", 5) + "quit")
		self.ws.close()

	def send(self, pid, msg):
		self.ws.send(pack(">i", pid)+msg)

	def on_message(self, ws, message):
		pid = unpack(">i", message[:1])[0]
		message = message[1:]
		self.messages[pid].append(message)
		self.newMsg.emit()

	def getMessages(self, pid):
		out = []
		for i in self.messages[pid]:
			out.append(i)
			out.remove(i)
		return out

	def on_error(self, ws, error):
		print error

	def on_close(self, ws):
		print "### closed ###"
