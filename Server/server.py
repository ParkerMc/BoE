from socket import *
from threading import Thread
from os import path
import datetime
global running
running = True
global file
file = False
global ftext
ftext = []
def addToFile(text):
	global file
	global ftext
	if not file:
		if path.isfile("chat/Main/"+str(datetime.date.today())): 
			file = open("chat/Main/"+str(datetime.date.today()),"r")
			ftext = file.readlines()
			file.close()
			file = open("chat/Main/"+str(datetime.date.today()),"w")
			file.write("".join(ftext))

		else:
			ftext = []
			file = open("chat/Main/"+str(datetime.date.today()),"w")
	elif not path.isfile("chat/Main/"+str(datetime.date.today())):
		file.close()
		ftext = []
		file = open("chat/Main/"+str(datetime.date.today()),"w")
	if text != "":
		ftext.append(text+"\n")
		file.write(text+"\n")

def recieveData(conn):
	data = conn.recv(1024)	
	print conn, data, "\n"
	return data;

def broadcastData(data, name=None):
	global conns
	for i,j in conns:
		j.sendall(data)


def main():
	s = socket(AF_INET, SOCK_STREAM)
	s.bind(('localhost', 8000))
	s.listen(5) # number of connections listening for
	print "Server is running...... \n"
	global conns
	global threads
	threads = []
	threadi = 0
	conns = []
	try:
		while running:
			conn, addr = s.accept()
			conns.append((threadi,conn))
			data = recieveData(conn)
			addToFile("")
			global ftext
			print '\n'.join(ftext)
			conn.sendall("".join(ftext))
			broadcastData(data+"@"+addr[0]+ " is now connected! \n")
			f = open("chat/Main/welcome.chat","r")
			conn.sendall(f.readline())
			f.close()
			threads.append(Thread(target = addConnections, args = (conn, data, threadi, )))
			threads[threadi].start()
			threadi += 1;
	except KeyboardInterrupt:
		print "killed"

def addConnections(conn, name, tid):
	while running:
		try:
			data = recieveData(conn)
			if data == "quit":
				for i, j in conns:
					if i == tid: 
						conns.pop(i)
						broadcastData(name+" left.")
						j.close()
			else:
				addToFile(data)
				broadcastData(data)
		except Exception, e:
			for i, j in conns:
				if i == tid: 
					broadcastData(name+" left.")
					conns.pop(i)
					j.close()
main()
