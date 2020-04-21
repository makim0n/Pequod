#!/usr/bin/python3

from flask import Flask
from pequod_database import *

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/items')
def get_item():
    resultqry = db.session.query(Files).all()
    print(resultqry)
    for i in resultqry:
        print(i.owner)
    return "TEMPLATE IS BETTER, LOOK AT YOUR CONSOLE"