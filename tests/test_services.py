from datetime import timedelta, date
import pytest

from app.services import time_point_calculation


@pytest.mark.parametrize("days_from_today, expected_result", [
    (1, 8),
    (2, 16),
    (3, 24),
])
def test_time_point_calculation(days_from_today, expected_result):
    test_date = date.today() + timedelta(days_from_today)
    total_count = time_point_calculation(test_date)
    assert total_count == expected_result


def test_call_weather_api():
    assert False


def test_isolate_day_data():
    assert False


def test_pull_weather_data():
    assert False


def test_clean_weather_data():
    assert False


def test_date_model():
    assert False
