import socket
import time
ip ="0.0.0.0"
port = 21
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip,port))
sock.listen(10)
while 1:
	client, addr = sock.accept()
	filename=client + " -" +time.strftime("%d/%m/%Y")
	fp = open(filename,"w")
	lung = client.recv(1024)
	for i in range(0,lung):
		c = client.recv(1024)
		testo = testo + c 
	fp.write(testo)
	fp.close()
