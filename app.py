#!/usr/bin/env python

from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import socket
import json 

app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
        return redirect(url_for('login'))
    else:
        return render_template('update.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect(url_for('update'))
    else:
        return render_template('login.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    data = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1",34567))
    while True:            
        data_b = sock.recv(4096)
        data = json.loads(data_b.decode('utf-8'))
        return render_template('update.html', data = data)
        print("hello")
        if request.form['submit'] == 'ddosattack':
            submit_req = request.form['submit']
            sock.send(submit_req.encode('utf-8'))
        
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.debug=True
    app.run()