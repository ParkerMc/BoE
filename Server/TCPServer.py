import socket, ssl, modloader

from threading import Thread

class TCPSocket(object):

	def __init__(self, server, conn, address):
		self.newid = server.mods.newid
		self.server = server
		self.address = address
		self.conn = conn
		self.data = ""
		self.pId = 0

	def handle(self):
		self.server.mods.Cinit(self, self.server)
		self.handleConnected()
		while True:
			try:
				data = self.conn.recv(1024)
			except Exception, e:
				if self.data != "quit":
					self.close()
					raise e
				return
			self.pId = data[:1]
			self.data = data[1:]
			self.handleMessage()

	def handleMessage(self):
		"""
			Called when data is received.
			To access the data call self.data.
		"""
		pass

	def handleConnected(self):
		"""
			Called when a client connects to the server.
		"""
		pass

	def handleClose(self):
		"""
			Called when a server gets a Close frame from a client.
		"""
		pass

	def close(self, status = 1000, reason = u''):
		"""
			Close
		"""
		self.server.mods.Cclose(self,self.server)
		self.handleClose()
		self.conn.close()
	def send(self, data):
		"""
			Send data to the client.
		"""
		self.conn.sendall(data)
		

class TCPServer(object):
	def __init__(self, host, port, websocketclass):
		print "loading mods(if any)"
		self.mods = modloader()
		self.running = True
		self.websocketclass = websocketclass
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind((host, port))
		self.serversocket.listen(5)
		self.connections = []
		self.threads = {}


	def close(self):
		self.mods.Sclose(self)
		for handle, conn in self.connections:
			conn.close()
			conn.handleClose()
		self.serversocket.close()

	def listener(self):
		while self.running:
			conn, addr = self.serversocket.accept()
			targetClass = self.websocketclass(self,conn,addr)
			self.connections.append((targetClass, conn))
			self.threads[addr] = Thread(target = targetClass.handle(), args = ( ), name=str(addr)) # Add threads
			self.threads[addr].start() # Start thread

	def serveforever(self):
		self.mods.Sinit(self)
		self.listenerT = Thread(target = self.listener, args = ( ),name='listener') # Add threads
		self.listenerT.start()
		while self.running:
			if raw_input('Type "close" to close') == "close":
				self.running = False
				self.close()
				break
			


class SSLTCPServer(TCPServer):

	def __init__(self, host, port, websocketclass, sslfile):
		print "loading mods(if any)"
		self.mods = modloader.modloader()
		import inspect
		print inspect.getmembers(self.mods, predicate=inspect.isfunction)
		self.running = True
		self.websocketclass = websocketclass
		self.uwserversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.uwserversocket.bind((host, port))
		self.uwserversocket.listen(5)
		self.serversocket = ssl.wrap_socket(self.uwserversocket, keyfile=sslfile, certfile=sslfile)
		self.connections = []
		self.threads = {}

	def close(self):
		self.mods.Sclose(self)
		for handle, conn in self.connections:
			conn.close()
			conn.handleClose()
		self.uwserversocket.close()
