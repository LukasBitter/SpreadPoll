#!/usr/bin/python
# coding: utf-8

from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
app = Flask(__name__)

@app.route('/')
def poll_list():
    worksheet_list = spreadsheet.worksheets()
    return render_template('home.html', polls=worksheet_list )

@app.route('/<poll_slug>', methods=['GET'])
def display_poll(poll_slug):
    try:
        poll = spreadsheet.worksheet(poll_slug)
    except gspread.exceptions.WorksheetNotFound:
        return "Sorry, no poll at that url", 404

    options = poll.row_values(1)
    title = options.pop(0)

    return render_template('poll.html', **locals())

@app.route('/<poll_slug>', methods=['POST'])
def vote(poll_slug):
    try:
        poll = spreadsheet.worksheet(poll_slug)
    except gspread.exceptions.WorksheetNotFound:
        return "Sorry, no poll at that url", 404

    voter = request.form['who']
    poll.insert_row([voter], index=2)
    return redirect(url_for('display_poll', poll_slug=poll_slug))

if __name__ == '__main__':

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Polls-b1f556282d93.json', scope)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open("Polls")

    app.run(debug=True) # désactiver le debug en production!!!