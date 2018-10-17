import time

def recvTimeout(sock, timeout=5):
    sock.setblocking(0)
    total_data = [];
    begin = time.time()
    
    while 1:
        if total_data and time.time() - begin > timeout:
            break
        elif time.time() - begin > timeout*2:
            break
        try:
            data = sock.recv(8192)
            if data:
                data = data.decode('utf-8')
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.3)
        except:
            pass
     
    return ''.join(total_data).replace('\n', '</br>')
