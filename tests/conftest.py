import json
from pathlib import Path
from typing import Any, Dict, Generator

import pytest
from faker import Faker

from src.client.booking_client import BookingClient
from src.config import settings

fake = Faker()

DATA_DIR = Path(__file__).parent / "data"



# Core client / auth fixtures
@pytest.fixture(scope="session")
def api_client() -> BookingClient:
    """One HTTP session (with retry adapter) reused across the whole run."""
    return BookingClient(base_url=settings.BASE_URL)


@pytest.fixture(scope="session")
def auth_token(api_client: BookingClient) -> str:
    """Create an auth token once per session and reuse it for write calls."""
    response = api_client.create_token(
        settings.AUTH_USERNAME, settings.AUTH_PASSWORD
    )
    assert response.status_code == 200, f"Failed to authenticate: {response.text}"
    return response.json()["token"]


@pytest.fixture()
def authenticated_client(api_client: BookingClient, auth_token: str) -> BookingClient:
    """Client with the auth cookie attached — required for PUT/PATCH/DELETE."""
    api_client.set_auth_cookie(auth_token)
    return api_client


# Test data factories
@pytest.fixture()
def booking_payload_factory():
    """Factory fixture: call it (optionally with overrides) to get a fresh,
    randomized, schema-valid booking payload for each test.
    """

    def _make(**overrides: Any) -> Dict[str, Any]:
        payload = {
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "totalprice": fake.random_int(min=50, max=2000),
            "depositpaid": fake.boolean(),
            "bookingdates": {
                "checkin": "2025-01-01",
                "checkout": "2025-01-10",
            },
            "additionalneeds": fake.word(),
        }
        payload.update(overrides)
        return payload

    return _make


@pytest.fixture()
def booking_payload(booking_payload_factory) -> Dict[str, Any]:
    return booking_payload_factory()


@pytest.fixture()
def created_booking(
    authenticated_client: BookingClient, booking_payload: Dict[str, Any]
) -> Generator[Dict[str, Any], None, None]:
    """Create a booking, yield {id, payload} to the test, then always clean
    it up afterwards — regardless of whether the test passed or failed.
    """
    response = authenticated_client.create_booking(booking_payload)
    assert response.status_code == 200, f"Setup failed: {response.text}"
    booking_id = response.json()["bookingid"]

    yield {"id": booking_id, "payload": booking_payload}

    authenticated_client.delete_booking(booking_id)



# Dynamic parametrization: contract test cases are data-driven, not
# hardcoded, so adding a new case means editing JSON, not Python.
def pytest_generate_tests(metafunc):
    if "contract_case" in metafunc.fixturenames:
        with open(DATA_DIR / "booking_payloads.json") as f:
            cases = json.load(f)
        metafunc.parametrize(
            "contract_case",
            cases,
            ids=[case["name"] for case in cases],
        )
