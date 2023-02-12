from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_weather_data():
    params = {
        "city_name": "Los Angeles",
        "request_date": str(date.today() + timedelta(1))
    }
    response = client.get(f"/weather_forecast", params=params)
    assert response.status_code == 200
