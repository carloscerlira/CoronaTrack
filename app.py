import requests
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/example')
def example():
    return render_template('exampleTemplate.html')

@app.route('/country/<string:country>')
def country(country):
    data_url = f'https://raw.githubusercontent.com/carloscerlira/CoronaTrack/master/data/time_series/{country}.json'
    data = requests.get(data_url).json()
    return render_template('countryInfo.html', data=data)   

if __name__ == '__main__':
    app.run(debug=True)