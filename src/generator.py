import json
import random

def load_data(filename):
    with open(f'data/{filename}', 'r') as file:
        return json.load(file)

def generate_motivation(day_of_week, day_of_month, year):
    quotes = load_data('quotes.json')
    tips = load_data('tips.json')

    # Простая логика выбора на основе дня недели
    quote = quotes[day_of_week % len(quotes)]

    # Выбор совета на основе дня месяца
    tip = tips[day_of_month % len(tips)]

    return f"{quote} {tip}"
