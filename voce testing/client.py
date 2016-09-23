import socket

import pyaudio

# record
CHUNK = 512  # 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050  # 44100
RECORD_SECONDS = 10

HOST = 'localhost'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOST, PORT))
send_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print send_buffer_size
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("*recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    s.sendall(data)
s.sendall("")
print("*done recording")

stream.stop_stream()
stream.close()
p.terminate()
s.close()

print("*closed")
