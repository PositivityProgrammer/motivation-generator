import sys
import os
from pathlib import Path
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
import json

# Добавляем путь к src в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from app import app
from generator import generate_motivation, load_data

# Тестовые данные для моков
mock_quotes = [
    "Вір у себе, і все можливо!",
    "Кожен день - це нова можливість.",
    "Ти сильніший, ніж ти думаєш.",
    "Мрій великими мріями.",
    "Ніколи не здавайся!",
    "Твоє ставлення визначає твою висоту.",
    "Будь змінами, які ти хочеш бачити у світі."
]

mock_tips = [
    "Почни свій день з позитивної думки.",
    "Зроби щось добре для себе сьогодні.",
    "Не забудь подякувати комусь сьогодні.",
    "Приділи час своєму хобі.",
    "Зроби маленький крок до своєї мети."
]

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_data_files(monkeypatch):
    def mock_load_data(filename):
        if filename == 'quotes.json':
            return mock_quotes
        elif filename == 'tips.json':
            return mock_tips
        raise FileNotFoundError(f"No mock data for {filename}")

    monkeypatch.setattr('generator.load_data', mock_load_data)

def test_get_motivation(client, mock_data_files):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "motivation" in data
    motivation = data["motivation"]
    assert any(quote in motivation for quote in mock_quotes)
    assert any(tip in motivation for tip in mock_tips)

def test_generate_motivation(mock_data_files):
    for day in range(7):  # test for each day of the week
        motivation = generate_motivation(day, 1, 2023)
        assert mock_quotes[day % len(mock_quotes)] in motivation
        assert any(tip in motivation for tip in mock_tips)

def test_generate_motivation_different_days(mock_data_files):
    motivation1 = generate_motivation(0, 1, 2023)  # Monday
    motivation2 = generate_motivation(1, 1, 2023)  # Tuesday
    assert motivation1 != motivation2

def test_generate_motivation_same_day_different_month(mock_data_files):
    motivation1 = generate_motivation(0, 1, 2023)  # 1st of the month
    motivation2 = generate_motivation(0, 2, 2023)  # 2nd of the month
    assert motivation1 != motivation2

def test_load_data():
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_quotes))):
        data = load_data('quotes.json')
        assert data == mock_quotes

def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data('nonexistent.json')
