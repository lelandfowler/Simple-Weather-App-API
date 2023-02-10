from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_weather_data():
    params = {
        "request_date": str(date.today() + timedelta(1))
    }
    city_name = 'Los Angeles'
    response = client.get(f"/{city_name}", params=params)
    assert response.status_code == 200
