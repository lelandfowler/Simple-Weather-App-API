from datetime import timedelta, date

import pytest

from app.services import time_point_calculation


@pytest.mark.parametrize("days_from_today, expected_result", [
    (1, [0, 6]),
    (2, [7, 15]),
    (3, [16, 23]),
])
def test_time_point_calculation(days_from_today, expected_result):
    test_date = date.today() + timedelta(days_from_today)
    first_time_point_index, last_time_point_index = time_point_calculation(test_date)
    assert first_time_point_index == expected_result[0]
    assert last_time_point_index == expected_result[1]


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
