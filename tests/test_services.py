from datetime import timedelta, date
import pytest
from fastapi import HTTPException
from app.services import time_point_calculation, DateModel, call_weather_api, isolate_day_data, clean_weather_data


@pytest.mark.parametrize("days_from_today, expected_result", [
    (1, 8),
    (2, 16),
    (3, 24),
])
def test_time_point_calculation(days_from_today, expected_result):
    test_date = date.today() + timedelta(days_from_today)
    total_count = time_point_calculation(test_date)
    assert total_count == expected_result


def test_call_weather_api_gets_good_response():
    city_name = 'London'
    total_count = 1
    try:
        call_weather_api(city_name, total_count)
    except Exception as e:
        pytest.fail(f"Unexpected Error: {e}")


def test_call_weather_api_bad_input_fails():
    city_name = 'Londo'
    total_count = 1
    with pytest.raises(HTTPException):
        call_weather_api(city_name, total_count)


def test_isolate_day_data():
    request_data = {
        "list": [
            {
                'dt_txt': '2023-02-10 01:00:00',
                'good_data': True
            },
            {
                'dt_txt': '2023-02-10 02:00:00',
                'good_data': True
            },
            {
                'dt_txt': '2023-02-11 01:00:00',
                'good_data': False
            },
            {
                'dt_txt': '2023-02-11 02:00:00',
                'good_data': False
            },
        ]
    }
    request_date = '2023-02-10'
    test_set = [
        {
            'dt_txt': '2023-02-10 01:00:00',
            'good_data': True
        },
        {
            'dt_txt': '2023-02-10 02:00:00',
            'good_data': True
        },
    ]

    isolated_data = isolate_day_data(request_data, request_date)
    assert isolated_data == test_set


def test_clean_weather_data():
    input_data = [
        {'dt': 1676073600, 'main': {'temp': 44.76, 'feels_like': 41.86, 'temp_min': 44.76, 'temp_max': 44.76, 'pressure': 1036, 'sea_level': 1036, 'grnd_level': 1033, 'humidity': 94, 'temp_kf': 0}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'clouds': {'all': 100}, 'wind': {'speed': 5.3, 'deg': 242, 'gust': 15.73}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2023-02-11 00:00:00'},
        {'dt': 1676084400, 'main': {'temp': 44.96, 'feels_like': 42.39, 'temp_min': 44.96, 'temp_max': 44.96, 'pressure': 1035, 'sea_level': 1035, 'grnd_level': 1032, 'humidity': 92, 'temp_kf': 0}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'clouds': {'all': 100}, 'wind': {'speed': 4.88, 'deg': 259, 'gust': 14.41}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2023-02-11 03:00:00'},
    ]

    correct_output_data = {
        '2023-02-11 00:00:00': {'temp': 44.76, 'humidity': 94},
        '2023-02-11 03:00:00': {'temp': 44.96, 'humidity': 92},
    }

    assert clean_weather_data(input_data) == correct_output_data


@pytest.mark.parametrize("good_request_dates", [
    date.today() + timedelta(1),
    date.today() + timedelta(2),
    date.today() + timedelta(3),
])
def test_date_model_allows_dates_within_range(good_request_dates):
    try:
        DateModel.parse_obj({"date": good_request_dates})
    except Exception as e:
        pytest.fail(f"Unexpected Error: {e}")


@pytest.mark.parametrize("bad_request_dates", [
    date.today() - timedelta(1),
    date.today() + timedelta(4),
])
def test_data_model_dates_catches_out_of_range_dates(bad_request_dates):
    with pytest.raises(HTTPException):
        DateModel.parse_obj({"date": bad_request_dates})
