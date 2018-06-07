#!/usr/bin/env python
#Python bot sample

import socket
BUFF = 4096

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',8080))
    sock.send(b'ciao')
    while True:
        print("I'm waiting for something...")
        data = sock.recv(BUFF)
        if data:
            print('data: ' +data.decode('utf-8'))

if __name__ == '__main__':
    main()
