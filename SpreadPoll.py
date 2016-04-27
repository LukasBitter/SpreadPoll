#!/usr/bin/python
# coding: utf-8

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! flask hello'

if __name__ == '__main__':
    app.run(debug=True) # désactiver le debug en production!!!