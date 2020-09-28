import requests
import json
from flask import Flask, render_template, url_for, request
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
load_dotenv()
import os
from getData import updateData

app = Flask(__name__)
scheduler = APScheduler()

@app.route('/')
def home():
    table_url = 'https://raw.githubusercontent.com/carloscerlira/CoronaTrack/master/data/general.json'
    table = requests.get(table_url).json()
    return render_template('home.html', table=table)

@app.route('/aboutData')
def aboutData():
    return render_template('aboutData.html')

@app.route('/aboutCOVID')
def aboutCOVID():
    return render_template('aboutCOVID.html')

@app.route('/country/<string:country>')
def country(country):
    data_url = f'https://raw.githubusercontent.com/carloscerlira/CoronaTrack/master/data/time_series/{country}.json'
    data = requests.get(data_url).json()
    return render_template('countryInfo.html', data=data)   

@app.route('/test')
def test():
    return render_template('test.html')

def scheduledTask():
    user = os.getenv('user')
    password = os.getenv('password')
    updateData(user, password)

scheduler.add_job(id='Scheduled task', func=scheduledTask, trigger='cron', timezone='UTC', hour=0, minute=20)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)