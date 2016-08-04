from socket import *
from threading import Thread

def recieveData(conn):
	data = conn.recv(1024)
	print conn, data, "\n"
	return data;

def broadcastData(data):
	global conns
	for i,j in conns:
		j.sendall(data)
	print "Data sent to all clients \n"

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
	while True:
		conn, addr = s.accept()
		conns.append((threadi,conn))
		data = recieveData(conn)
		broadcastData(data+"@"+addr[0]+ " is now connected! \n")
		threads.append(Thread(target = addConnections, args = (conn, data, threadi, )))
		threads[threadi].start()
		threadi += 1;


def addConnections(conn, name, tid):
	while True:
		data = recieveData(conn)
		print("loop")
		if data == "quit":
			for i, j in conns:
				if i == tid: 
					broadcastData(name+" left.")
					conns.pop(i)
					j.close()
		broadcastData(data)


main()