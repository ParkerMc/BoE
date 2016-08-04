from socket import *
from threading import Thread

def recieveData(conn):
	data = conn.recv(1024)
	print conn, data, "\n"
	return data;

def broadcastData(conn, data):
	global conns
	for i,j in conns:
		j.sendall(data)
	print "Data sent to all clients \n"

def main():
	s = socket(AF_INET, SOCK_STREAM)
	s.bind(('localhost', 8000))
	s.listen(5) # number of connections listening for
	print "Server is running...... \n"
	threads = []
	threadi = 0
	global conns
	conns = []
	while True:
		conn, addr = s.accept()
		conns.append((threadi,conn))
		print addr, " is now connected! \n"
		threads.append(Thread(target = addConnections, args = (conn, threadi, )))
		threads[threadi].start()
		threadi += 1;


def addConnections(conn, id):
	while True:
		data = recieveData(conn)
		broadcastData(conn,  data)


main()