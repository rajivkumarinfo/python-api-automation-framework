import allure
import pytest

from src.client.booking_client import BookingClient


@allure.epic("Restful-Booker")
@allure.feature("Health")
@pytest.mark.smoke
def test_ping_returns_201(api_client: BookingClient):
    """The health-check endpoint should confirm the API is up."""
    with allure.step("Call GET /ping"):
        response = api_client.ping()

    assert response.status_code == 201, (
        f"Expected 201 from /ping, got {response.status_code}"
    )
