#!/usr/bin/env python

import socket
import string 
import select 
import json 

host = '0.0.0.0'
port = 34567
sock_by_ip = {}
catch_ip = []

def run(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    sock.setblocking(0)
    print('[*] Server listen on %s:%d' % (host,port))
    print('[*] Enstablish connection with clients')
    inputs = [sock]
    outputs = []
    x = 0
    
    while inputs:
        readable, writable, error = select.select(inputs, outputs, [])
        if len(readable) != 0:
            for fds in readable:
                 if fds is sock:
                    connection, addr = fds.accept()
                    inputs.append(connection)
                    catch_ip.append(addr)
                    data = json.dumps(catch_ip)
                    sock_by_ip[addr[0]] = inputs[x]
                    x += 1
                    print("SOCK IP")
                    print(sock_by_ip)
                    print("CATCH IP")
                    print(catch_ip)
                    print("INPUTS")
                    print(inputs)
                    
                    # Check if the input address is the connection from the Flask server
                    if addr[0] == '127.0.0.1':
                        connection.send(data.encode('utf-8'))
                 
                 #else:
                    #data = connection.recv(1024)
                    #data_list = data.decode('utf-8')
                    #data_list = data.split(':')
                    
                    #if not data:
                        #inputs.remove(fds)
                    #else:
                        #for fds in writable:
                            #write_sock = sock_by_ip[data_list[1]]
                            #write_sock.send(data_list)


if __name__ == '__main__':
    run(host, port)
