from flask import Flask,request, jsonify
import requests
import os
from dotenv import load_dotenv

app=Flask(__name__)

load_dotenv()

MY_CITY=os.getenv('CITY')
X_TOKEN=os.getenv('X-TOKEN')


@app.route('/temperature', methods=['GET'])
def get_temperature():

    url = f'https://api.openweathermap.org/data/2.5/weather?q={MY_CITY}&appid={X_TOKEN}'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or data.get('cod') != 200:
        return jsonify(error="Failed to fetch temperature data"), 500

    temperature = round(data['main']['temp'] - 273.15)
    return jsonify(temperature=temperature), 200


@app.route('/temperature/history', methods=['GET'])
def get_temperature_history():
    day = input('Please enter day:')
    x_token = request.headers.get('x-token')

    if x_token != X_TOKEN:
        return jsonify(error="Unauthorized access"), 401

    if not day:
        return jsonify(error="Day not specified"), 400


    url = f'https://api.openweathermap.org/data/2.5/weather?q={MY_CITY}&appid={X_TOKEN}'
    response = requests.get(url)
    data = response.json()
    lat = data['coord']['lat']
    lon = data['coord']['lon']

    url = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={day}&appid={X_TOKEN}'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or data.get('cod') != 200:
        return jsonify(error="Failed to fetch temperature history"), 500

    temperature_history = [hour_data['temp'] for hour_data in data['hourly']]
    return jsonify(temperature_history=temperature_history), 200


if __name__ == '__main__':
    app.run(debug=True)