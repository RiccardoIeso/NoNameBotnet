#!/usr/bin/env python

import socket
import string 
import select 
import json 

host = '127.0.0.1'
port = 34567
sock_by_ip = {}

def start_server(host, port, sock_by_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    sock.setblocking(0)
    print('[*] Server listen on %s:%d' % (host,port))
    print('[*] Enstablish connection with clients')
    inputs = [sock]
    outputs = []
    catch_ip = [] # List of all ip connected
    x = 0
    
    while inputs:
        readable, writable, error = select.select(inputs, outputs, [])
        if len(readable) != 0:
            for fds in readable:
                 if fds is sock:
                    connection, addr = fds.accept()
                    inputs.append(connection)
                    catch_ip.append(addr[0])
                    data = json.dumps(catch_ip)
                    sock_by_ip[addr[0]] = inputs[x]
                    x += 1
                    print(sock_by_ip)
                    print(catch_ip)
                    
                    if addr[0] == '127.0.0.1':
                        connection.send(data.encode('utf-8'))
                 else:
                    data = connection.recv(1024)
                    data_list = data.decode('utf-8')
                    data_list = data.split(':')
                    
                    if not data:
                        inputs.remove(fds)
                    else:
                        for fds in writable:
                            write_sock = sock_by_ip[data_list[1]]
                            write_sock.send(data_list)


if __name__ == '__main__':
    start_server(host, port, sock_by_ip)
