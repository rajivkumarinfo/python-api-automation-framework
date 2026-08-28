# Contract tests: response shape must match the published JSON Schema for every case in tests/data/booking_payloads.json.

# Cases are injected dynamically via the `pytest_generate_tests` hook in
# conftest.py — add a new case to the JSON file and it is picked up with no code changes.

import allure
import pytest

from src.client.booking_client import BookingClient
from src.schemas.booking_schema import CREATE_BOOKING_RESPONSE_SCHEMA
from src.utils.schema_validator import assert_matches_schema


@allure.epic("Restful-Booker")
@allure.feature("Contract validation")
@pytest.mark.contract
def test_create_booking_matches_contract(
    authenticated_client: BookingClient, contract_case: dict
):
    payload = contract_case["payload"]

    with allure.step(f"Create booking: {contract_case['name']}"):
        response = authenticated_client.create_booking(payload)

    assert response.status_code == 200
    body = response.json()

    assert_matches_schema(body, CREATE_BOOKING_RESPONSE_SCHEMA)

    for field, expected in payload.items():
        assert body["booking"].get(field) == expected, (
            f"Field '{field}' mismatch for case '{contract_case['name']}'"
        )

    authenticated_client.delete_booking(body["bookingid"])
