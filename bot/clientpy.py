#!/usr/bin/env python

import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',8081))
    while True:
        data = sock.recv(4096)
        print(data)

if __name__ == '__main__':
    main()
