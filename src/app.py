import os
from flask import Flask, jsonify
from datetime import datetime
from generator import generate_motivation

app = Flask(__name__)

@app.route('/')
def get_motivation():
    today = datetime.now()
    day_of_week = today.weekday()
    day_of_month = today.day
    year = today.year

    motivation = generate_motivation(day_of_week, day_of_month, year)
    return jsonify({"motivation": motivation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
